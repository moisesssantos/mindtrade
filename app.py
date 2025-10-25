import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# ===============================
# CONFIGURAÇÃO INICIAL
# ===============================

st.set_page_config(page_title="MindTrade", layout="wide")

# URL do banco Neon (segura via variável de ambiente)
DATABASE_URL = st.secrets.get("DATABASE_URL")

if not DATABASE_URL:
    st.error("⚠️ A variável DATABASE_URL não está configurada. Adicione-a em 'Secrets'.")
    st.stop()

# Cria engine SQLAlchemy
engine = create_engine(DATABASE_URL)

# ===============================
# INTERFACE
# ===============================
st.title("💡 MindTrade — Painel de Controle")
st.markdown("### Conectado ao banco Neon via SQLAlchemy")

# ===============================
# TESTE DE CONEXÃO
# ===============================
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT NOW() as current_time"))
        data = result.fetchone()
        st.success(f"✅ Conexão bem-sucedida! Hora atual do servidor: {data[0]}")
except Exception as e:
    st.error(f"❌ Erro ao conectar ao banco: {e}")

# ===============================
# EXEMPLO DE LEITURA DE TABELAS
# ===============================
st.subheader("📋 Tabelas disponíveis no banco")

try:
    query = """
    SELECT table_name 
    FROM information_schema.tables
    WHERE table_schema = 'public'
    ORDER BY table_name;
    """
    tables = pd.read_sql_query(query, engine)
    st.dataframe(tables)
except Exception as e:
    st.error(f"Erro ao listar tabelas: {e}")
