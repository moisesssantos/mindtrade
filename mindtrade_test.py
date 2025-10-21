import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# -----------------------------------------
# CONFIGURAÇÃO INICIAL
# -----------------------------------------
st.set_page_config(page_title="MindTrade - Dashboard", layout="wide", page_icon="📊")

# Tema escuro customizado
st.markdown("""
    <style>
        body {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .stApp {
            background-color: #0E1117;
        }
        h1, h2, h3 {
            color: #00C0F3;
        }
        .metric-card {
            background-color: #1E222A;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0px 0px 15px rgba(0,192,243,0.1);
            transition: 0.3s;
        }
        .metric-card:hover {
            transform: scale(1.03);
            box-shadow: 0px 0px 25px rgba(0,192,243,0.3);
        }
        .stButton > button {
            background-color: #00C0F3;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            font-size: 1.1em;
            font-weight: bold;
            margin-top: 10px;
            transition: 0.2s;
        }
        .stButton > button:hover {
            background-color: #008FB5;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------
# CONEXÃO COM O BANCO
# -----------------------------------------
engine = create_engine(
    "postgresql://neondb_owner:npg_xdZKq5FRT8Wn@ep-dry-wind-adh6ysjv-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

# -----------------------------------------
# CABEÇALHO
# -----------------------------------------
st.title("📊 MindTrade Dashboard")
st.markdown("Visual inspirado em *Seattle Weather*, agora no tema escuro do MindTrade ⚡")

# -----------------------------------------
# SIMULAÇÃO DE DADOS (ainda será ligada ao Neon)
# -----------------------------------------
np.random.seed(42)
dias = pd.date_range("2025-01-01", periods=30)
lucros = np.random.normal(0, 100, 30).cumsum() + 1000
greens = np.random.randint(0, 10, 30)
reds = np.random.randint(0, 10, 30)
df = pd.DataFrame({"Data": dias, "Lucro_Acumulado": lucros, "Greens": greens, "Reds": reds})

# -----------------------------------------
# LAYOUT DE MÉTRICAS
# -----------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric("💰 Lucro Total", f"R$ {df['Lucro_Acumulado'].iloc[-1]:.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric("✅ Greens", int(df["Greens"].sum()))
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric("❌ Reds", int(df["Reds"].sum()))
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------------
# GRÁFICO PRINCIPAL
# -----------------------------------------
st.subheader("📈 Evolução do Lucro Acumulado")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df["Data"], df["Lucro_Acumulado"], color="#00C0F3", linewidth=2.5)
ax.set_facecolor("#1E222A")
ax.grid(True, linestyle="--", alpha=0.4, color="#666")
ax.set_xlabel("Data", color="white")
ax.set_ylabel("Lucro (R$)", color="white")
ax.tick_params(colors="white")
fig.patch.set_facecolor("#0E1117")
st.pyplot(fig)

# -----------------------------------------
# SEGUNDO GRÁFICO
# -----------------------------------------
st.subheader("📊 Comparativo de Greens e Reds")

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.bar(df["Data"], df["Greens"], color="#2ca02c", alpha=0.8, label="Greens")
ax2.bar(df["Data"], -df["Reds"], color="#d62728", alpha=0.8, label="Reds")
ax2.legend(facecolor="#0E1117", labelcolor="white")
ax2.set_facecolor("#1E222A")
ax2.grid(True, linestyle="--", alpha=0.4, color="#666")
ax2.set_xlabel("Data", color="white")
ax2.set_ylabel("Quantidade", color="white")
ax2.tick_params(colors="white")
fig2.patch.set_facecolor("#0E1117")
st.pyplot(fig2)

# -----------------------------------------
# RODAPÉ
# -----------------------------------------
st.markdown("---")
st.caption("💠 MindTrade © 2025 — Painel estilo Seattle Weather com tema escuro profissional.")
