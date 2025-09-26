import streamlit as st
import pandas as pd
import plotly.express as px

# === Carregar dados ===
df = pd.read_csv("julgados_1.csv", sep=",", decimal=".")

st.set_page_config(page_title="Dashboard de Julgados", layout="wide")
st.title("📊 Dashboard de Julgados Fictícios")
st.markdown("Explore os julgados e identifique possíveis erros de coleta e inconsistências.")

# === Criar colunas de análise de erros ===
df["erro_tribunal"] = df["tribunal"].isna() | (df["tribunal"] == "") | (df["tribunal"] == "XXX")
df["erro_relator"] = df["relator"].isna() | (df["relator"] == "")
df["erro_assunto"] = df["assunto"].isna() | (df["assunto"] == "") | (df["assunto"] == "INDEFINIDO")
df["erro_decisao"] = df["decisao"].isna() | (df["decisao"] == "")
df["erro_data"] = pd.to_datetime(df["data_distribuicao"], errors="coerce").isna() | pd.to_datetime(df["data_julgamento"], errors="coerce").isna()
df["erro_ementa"] = df["ementa"].isna() | (df["ementa"].str.contains("ERRO", na=False))
df["erro_valor"] = df["valor_acao"] < 0
df["erro_coleta_geral"] = df[["erro_tribunal", "erro_relator", "erro_assunto", "erro_decisao", "erro_data", "erro_ementa", "erro_valor"]].any(axis=1)

# === Filtros laterais ===
st.sidebar.header("Filtros")
tribunais = st.sidebar.multiselect("Tribunal:", df["tribunal"].dropna().unique())
relatores = st.sidebar.multiselect("Relator:", df["relator"].dropna().unique())
assuntos = st.sidebar.multiselect("Assunto:", df["assunto"].dropna().unique())
decisoes = st.sidebar.multiselect("Decisão:", df["decisao"].dropna().unique())
varas_origem = st.sidebar.multiselect("Vara de Origem:", df["vara_origem"].dropna().unique())
recurso_interposto = st.sidebar.multiselect("Recurso Interposto:", df["recurso_interposto"].dropna().unique())
filtro_erros = st.sidebar.checkbox("Mostrar apenas registros com erros")

# Aplicar filtros
df_filtrado = df.copy()
if tribunais:
    df_filtrado = df_filtrado[df_filtrado["tribunal"].isin(tribunais)]
if relatores:
    df_filtrado = df_filtrado[df_filtrado["relator"].isin(relatores)]
if assuntos:
    df_filtrado = df_filtrado[df_filtrado["assunto"].isin(assuntos)]
if decisoes:
    df_filtrado = df_filtrado[df_filtrado["decisao"].isin(decisoes)]
if varas_origem:
    df_filtrado = df_filtrado[df_filtrado["vara_origem"].isin(varas_origem)]
if recurso_interposto:
    df_filtrado = df_filtrado[df_filtrado["recurso_interposto"].isin(recurso_interposto)]
if filtro_erros:
    df_filtrado = df_filtrado[df_filtrado["erro_coleta_geral"]]

# === Métricas principais ===
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total de Julgados", len(df_filtrado))
col2.metric("Tribunais", df_filtrado["tribunal"].nunique())
col3.metric("Relatores", df_filtrado["relator"].nunique())
col4.metric("Registros com erro", df_filtrado["erro_coleta_geral"].sum())
col5.metric("Varas de Origem", df_filtrado["vara_origem"].nunique())

# === Gráficos ===
st.subheader("📈 Distribuição dos Julgados")
col1, col2 = st.columns(2)

with col1:
    fig1 = px.histogram(
        df_filtrado, x="tribunal", color="erro_coleta_geral",
        title="Julgados por Tribunal (erro destacado)", barmode="group"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.histogram(
        df_filtrado, x="assunto", color="erro_coleta_geral",
        title="Julgados por Assunto (erro destacado)", barmode="group"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("📊 Distribuição de Erros por Tipo")
tipos_erro = df_filtrado["erro_tipo"].value_counts().reset_index()
tipos_erro.columns = ["Tipo de Erro", "Quantidade"]
fig3 = px.bar(tipos_erro, x="Tipo de Erro", y="Quantidade", title="Tipos de Erros Mais Frequentes")
st.plotly_chart(fig3, use_container_width=True)

# === Tabela com destaque para erros ===
st.subheader("📑 Tabela de Julgados")
st.dataframe(df_filtrado)

# === Download ===
st.download_button(
    "📥 Baixar CSV Filtrado",
    df_filtrado.to_csv(index=False).encode("utf-8"),
    "julgados_filtrados_analise.csv",
    "text/csv",
    key="download-csv"
)
