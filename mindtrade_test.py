import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.title("🔗 Teste de Conexão - MindTradeDB")

engine = create_engine(
    "postgresql://neondb_owner:npg_xdZKq5FRT8Wn@ep-dry-wind-adh6ysjv-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

try:
    df = pd.read_sql("SELECT * FROM pre_analise LIMIT 5;", engine)
    st.success("✅ Conectado com sucesso ao banco de dados!")
    st.dataframe(df)
except Exception as e:
    st.error(f"❌ Erro ao conectar: {e}")
