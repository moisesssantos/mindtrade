import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# -----------------------------------------
# CONFIGURAÇÃO INICIAL
# -----------------------------------------
st.set_page_config(page_title="MindTrade - Dashboard", layout="wide", page_icon="☁️")

st.title("☁️ MindTrade - Visão de Operações (Estilo Seattle Weather)")

# Conexão com o banco Neon
engine = create_engine(
    "postgresql://neondb_owner:npg_xdZKq5FRT8Wn@ep-dry-wind-adh6ysjv-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

# -----------------------------------------
# SIMULAÇÃO DE DADOS (você trocará depois pelos reais)
# -----------------------------------------
np.random.seed(42)
dias = pd.date_range("2025-01-01", periods=30)
lucros = np.random.normal(0, 100, 30).cumsum() + 1000
greens = np.random.randint(0, 10, 30)
reds = np.random.randint(0, 10, 30)

df = pd.DataFrame({"Data": dias, "Lucro_Acumulado": lucros, "Greens": greens, "Reds": reds})

# -----------------------------------------
# LAYOUT DE DESTAQUES
# -----------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("💰 Lucro Total", f"R$ {df['Lucro_Acumulado'].iloc[-1]:.2f}")
col2.metric("✅ Greens", df["Greens"].sum())
col3.metric("❌ Reds", df["Reds"].sum())

st.markdown("---")

# -----------------------------------------
# GRÁFICO PRINCIPAL
# -----------------------------------------
st.subheader("📈 Evolução do Lucro Acumulado")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df["Data"], df["Lucro_Acumulado"], color="#1f77b4", linewidth=2.5)
ax.set_facecolor("#f5f5f5")
ax.grid(True, linestyle="--", alpha=0.6)
ax.set_xlabel("Data")
ax.set_ylabel("Lucro (R$)")
st.pyplot(fig)

# -----------------------------------------
# SEGUNDO GRÁFICO
# -----------------------------------------
st.subheader("📊 Comparativo de Greens e Reds")
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.bar(df["Data"], df["Greens"], color="#2ca02c", alpha=0.7, label="Greens")
ax2.bar(df["Data"], -df["Reds"], color="#d62728", alpha=0.7, label="Reds")
ax2.legend()
ax2.set_xlabel("Data")
ax2.set_ylabel("Quantidade")
ax2.grid(True, linestyle="--", alpha=0.6)
st.pyplot(fig2)

st.markdown("---")
st.caption("💡 Visual inspirado em 'Seattle Weather' da Streamlit Gallery. Adaptado para o MindTrade © 2025.")
