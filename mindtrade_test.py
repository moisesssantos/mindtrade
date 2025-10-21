import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# -----------------------------------------
# CONFIGURAÇÕES INICIAIS
# -----------------------------------------
st.set_page_config(page_title="MindTrade", layout="wide")

# Conexão com o Neon
engine = create_engine(
    "postgresql://neondb_owner:npg_xdZKq5FRT8Wn@ep-dry-wind-adh6ysjv-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

st.title("🌍 Cadastro de Países")

# -----------------------------------------
# FORMULÁRIO DE CADASTRO
# -----------------------------------------
with st.form("form_paises"):
    nome = st.text_input("Nome do país")
    enviar = st.form_submit_button("Salvar País")

    if enviar:
        if nome.strip() == "":
            st.warning("⚠️ Digite o nome do país antes de salvar.")
        else:
            try:
                with engine.begin() as conn:
                    conn.execute(f"INSERT INTO paises (nome) VALUES ('{nome}')")
                st.success(f"✅ País '{nome}' adicionado com sucesso!")
            except Exception as e:
                st.error(f"❌ Erro ao inserir: {e}")

# -----------------------------------------
# EXIBIR TABELA DE PAÍSES
# -----------------------------------------
st.divider()
st.subheader("📋 Lista de Países Cadastrados")

try:
    df = pd.read_sql("SELECT * FROM paises ORDER BY id;", engine)
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"❌ Erro ao carregar países: {e}")
