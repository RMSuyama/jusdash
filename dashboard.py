import streamlit as st
import pandas as pd
import plotly.express as px

# === Login simples ===
senha_correta = "1234"  # Defina sua senha aqui
senha_usuario = st.sidebar.text_input("Digite a senha para acessar o dashboard:", type="password")

if senha_usuario != senha_correta:
    st.warning("Senha incorreta! Acesso negado.")
    st.stop()  # Impede o restante do código de rodar

# === Carregar dados ===
df = pd.read_csv("julgados_1.csv", sep=",", decimal=",")

st.set_page_config(page_title="Dashboard de Julgados", layout="wide")

st.title("📊 Dashboard de Julgados Fictícios")
st.markdown("Explore os julgados por tribunal, relator, assunto e decisão.")

# === Filtros laterais ===
st.sidebar.header("Filtros")

tribunais = st.sidebar.multiselect("Tribunal:", df["tribunal"].unique())
relatores = st.sidebar.multiselect("Relator:", df["relator"].unique())
assuntos = st.sidebar.multiselect("Assunto:", df["assunto"].unique())
decisoes = st.sidebar.multiselect("Decisão:", df["decisao"].unique())

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

# === Métricas principais ===
col1, col2, col3 = st.columns(3)
col1.metric("Total de Julgados", len(df_filtrado))
col2.metric("Tribunais", df_filtrado["tribunal"].nunique())
col3.metric("Relatores", df_filtrado["relator"].nunique())

# === Gráficos ===
st.subheader("📈 Distribuição dos Julgados")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.histogram(
        df_filtrado, x="tribunal", color="decisao",
        title="Julgados por Tribunal e Decisão", barmode="group"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.histogram(
        df_filtrado, x="assunto", color="tribunal",
        title="Julgados por Assunto", barmode="group"
    )
    st.plotly_chart(fig2, use_container_width=True)

# === Tabela ===
st.subheader("📑 Tabela de Julgados")
st.dataframe(df_filtrado)

# === Download ===
st.download_button(
    "📥 Baixar CSV Filtrado",
    df_filtrado.to_csv(index=False).encode("utf-8"),
    "julgados_filtrados.csv",
    "text/csv",
    key="download-csv"
)
