import streamlit as st
import pandas as pd
import plotly.express as px

# === Login simples ===
senha_correta = "1234"
senha_usuario = st.sidebar.text_input("Digite a senha para acessar o dashboard:", type="password")

if senha_usuario != senha_correta:
    st.warning("Senha incorreta! Acesso negado.")
    st.stop()

# === Carregar dados ===
df = pd.read_csv("julgados_1.csv", sep=",", decimal=",")

st.set_page_config(page_title="Dashboard de Julgados", layout="wide")

st.title("Dashboard de Julgados")
st.markdown("Explore os julgados e identifique possíveis erros de coleta e inconsistências.")

# === Mapa completo de tribunais ===
mapa_regioes = {
    # TJs - vinculados a estados
    "TJAC": "Norte", "TJAL": "Nordeste", "TJAP": "Norte", "TJAM": "Norte", "TJBA": "Nordeste",
    "TJCE": "Nordeste", "TJDFT": "Centro-Oeste", "TJES": "Sudeste", "TJGO": "Centro-Oeste",
    "TJMA": "Nordeste", "TJMT": "Centro-Oeste", "TJMS": "Centro-Oeste", "TJPB": "Nordeste",
    "TJPE": "Nordeste", "TJPI": "Nordeste", "TJPR": "Sul", "TJRJ": "Sudeste", "TJRN": "Nordeste",
    "TJRS": "Sul", "TJRO": "Norte", "TJRR": "Norte", "TJSC": "Sul", "TJSP": "Sudeste",
    "TJSE": "Nordeste", "TJTO": "Norte",

    # TRFs - regionais
    "TRF1": "Norte/Centro-Oeste", "TRF2": "Sudeste", "TRF3": "Sudeste",
    "TRF4": "Sul", "TRF5": "Nordeste",

    # Tribunais Superiores - nacionais
    "STF": "Nacional", "STJ": "Nacional", "TSE": "Nacional",
    "TST": "Nacional", "STM": "Nacional",

    # TREs (estaduais, seguem estados)
    "TRE-AC": "Norte", "TRE-AL": "Nordeste", "TRE-AP": "Norte", "TRE-AM": "Norte",
    "TRE-BA": "Nordeste", "TRE-CE": "Nordeste", "TRE-DF": "Centro-Oeste", "TRE-ES": "Sudeste",
    "TRE-GO": "Centro-Oeste", "TRE-MA": "Nordeste", "TRE-MT": "Centro-Oeste", "TRE-MS": "Centro-Oeste",
    "TRE-MG": "Sudeste", "TRE-PA": "Norte", "TRE-PB": "Nordeste", "TRE-PR": "Sul",
    "TRE-PE": "Nordeste", "TRE-PI": "Nordeste", "TRE-RJ": "Sudeste", "TRE-RN": "Nordeste",
    "TRE-RS": "Sul", "TRE-RO": "Norte", "TRE-RR": "Norte", "TRE-SC": "Sul",
    "TRE-SP": "Sudeste", "TRE-SE": "Nordeste", "TRE-TO": "Norte",

    # TRTs (regionais vinculados a estados, só exemplo simplificado)
    "TRT1": "Sudeste", "TRT2": "Sudeste", "TRT3": "Sudeste", "TRT4": "Sul", "TRT5": "Nordeste",
    "TRT6": "Nordeste", "TRT7": "Nordeste", "TRT8": "Norte", "TRT9": "Sul", "TRT10": "Centro-Oeste",
    "TRT11": "Norte", "TRT12": "Sul", "TRT13": "Nordeste", "TRT14": "Norte", "TRT15": "Sudeste",
    "TRT16": "Nordeste", "TRT17": "Sudeste", "TRT18": "Centro-Oeste", "TRT19": "Nordeste",
    "TRT20": "Nordeste", "TRT21": "Nordeste", "TRT22": "Nordeste", "TRT23": "Centro-Oeste",
    "TRT24": "Centro-Oeste", "TRT25": "Norte"
}

# Aplicar o mapeamento
df["regiao"] = df["tribunal"].map(mapa_regioes)

# === Criar colunas de análise de erros ===
df["erro_tribunal"] = df["tribunal"].isna() | (df["tribunal"] == "")
df["erro_relator"] = df["relator"].isna() | (df["relator"] == "")
df["erro_assunto"] = df["assunto"].isna() | (df["assunto"] == "")
df["erro_decisao"] = df["decisao"].isna() | (df["decisao"] == "")
df["erro_data"] = pd.to_datetime(df["data_distribuicao"], errors="coerce").isna() | pd.to_datetime(df["data_julgamento"], errors="coerce").isna()
df["erro_ementa"] = df["ementa"].isna() | (df["ementa"].str.contains("ERRO", na=False))
df["erro_geral"] = df[["erro_tribunal", "erro_relator", "erro_assunto", "erro_decisao", "erro_data", "erro_ementa"]].any(axis=1)

# Converter erro geral para "Com erro"/"Sem erro"
df["status_erro"] = df["erro_geral"].map({True: "Com erro", False: "Sem erro"})

# === Filtros laterais ===
st.sidebar.header("Filtros")
regioes = st.sidebar.multiselect("Região:", df["regiao"].dropna().unique())
tribunais = st.sidebar.multiselect("Tribunal:", df["tribunal"].dropna().unique())
relatores = st.sidebar.multiselect("Relator:", df["relator"].unique())
assuntos = st.sidebar.multiselect("Assunto:", df["assunto"].unique())
decisoes = st.sidebar.multiselect("Decisão:", df["decisao"].unique())
filtro_erros = st.sidebar.checkbox("Mostrar apenas registros com erro")

# Aplicar filtros
df_filtrado = df.copy()
if regioes:
    df_filtrado = df_filtrado[df_filtrado["regiao"].isin(regioes)]
if tribunais:
    df_filtrado = df_filtrado[df_filtrado["tribunal"].isin(tribunais)]
if relatores:
    df_filtrado = df_filtrado[df_filtrado["relator"].isin(relatores)]
if assuntos:
    df_filtrado = df_filtrado[df_filtrado["assunto"].isin(assuntos)]
if decisoes:
    df_filtrado = df_filtrado[df_filtrado["decisao"].isin(decisoes)]
if filtro_erros:
    df_filtrado = df_filtrado[df_filtrado["status_erro"] == "Com erro"]

# === Métricas principais ===
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Julgados", len(df_filtrado))
col2.metric("Tribunais", df_filtrado["tribunal"].nunique())
col3.metric("Relatores", df_filtrado["relator"].nunique())
col4.metric("Total de Valores (com erro)", (df_filtrado["status_erro"] == "Com erro").sum())

# === Gráficos ===
st.subheader("Distribuição dos Julgados")

# 🔹 Gráfico 1 - Barras horizontais por tribunal
erros_por_tribunal = df_filtrado.groupby(["tribunal", "status_erro"]).size().reset_index(name="total")
fig1 = px.bar(
    erros_por_tribunal.sort_values("total", ascending=True),
    x="total", y="tribunal", color="status_erro",
    orientation="h",
    title="Julgados por Tribunal (Com/Sem Erro)",
    labels={"total": "Quantidade", "tribunal": "Tribunal"}
)
st.plotly_chart(fig1, use_container_width=True)

# 🔹 Gráfico 2 - Regiões
fig2 = px.histogram(
    df_filtrado, x="regiao", color="status_erro",
    title="Julgados por Região (Com/Sem Erro)", barmode="group"
)
st.plotly_chart(fig2, use_container_width=True)

# === Tabela com destaque para erros ===
st.subheader("Tabela de Julgados")
st.dataframe(df_filtrado)

# === Download ===
st.download_button(
    "📥 Baixar CSV Filtrado",
    df_filtrado.to_csv(index=False).encode("utf-8"),
    "julgados_filtrados_analise.csv",
    "text/csv",
    key="download-csv"
)
