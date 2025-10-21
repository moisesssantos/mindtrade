import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

# -----------------------------------------
# CONFIGURAÇÕES INICIAIS
# -----------------------------------------
st.set_page_config(
    page_title="MindTrade - Países",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Tema escuro customizado (inspirado em Stock Peer Analysis)
st.markdown(
    """
    <style>
        body {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .stApp {
            background-color: #0E1117;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #00C0F3;
        }
        .css-1d391kg {
            background-color: #0E1117;
        }
        .stDataFrame {
            border: 1px solid #333;
            border-radius: 10px;
            padding: 10px;
            background-color: #1E222A;
        }
        .stButton > button {
            background-color: #00C0F3;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.5em 1em;
            font-weight: bold;
            transition: 0.2s;
        }
        .stButton > button:hover {
            background-color: #008FB5;
            transform: scale(1.02);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------
# CONEXÃO COM O BANCO
# -----------------------------------------
engine = create_engine(
    "postgresql://neondb_owner:npg_xdZKq5FRT8Wn@ep-dry-wind-adh6ysjv-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

# -----------------------------------------
# CABEÇALHO
# -----------------------------------------
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.title("🌍 Painel de Países")
    st.markdown("Gerencie os países cadastrados no sistema MindTrade com design inspirado em *Stock Peer Analysis*.")
with col2:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/2382/2382461.png",
        width=80,
    )

st.divider()

# -----------------------------------------
# FORMULÁRIO DE CADASTRO / EDIÇÃO
# -----------------------------------------
with st.container():
    st.subheader("➕ Adicionar / ✏️ Editar País")

    with st.form("form_paises", clear_on_submit=True):
        nome = st.text_input("Nome do país")
        id_editar = st.text_input("ID (para editar país existente)", "")
        enviar = st.form_submit_button("Salvar / Atualizar")

        if enviar:
            if nome.strip() == "":
                st.warning("⚠️ Digite o nome do país antes de salvar.")
            else:
                try:
                    with engine.begin() as conn:
                        if id_editar.strip() == "":
                            conn.execute(text("INSERT INTO paises (nome) VALUES (:nome)"), {"nome": nome})
                            st.success(f"✅ País '{nome}' adicionado com sucesso!")
                        else:
                            conn.execute(text("UPDATE paises SET nome = :nome WHERE id = :id"), {"nome": nome, "id": id_editar})
                            st.success(f"✏️ País ID {id_editar} atualizado para '{nome}'!")
                except IntegrityError:
                    st.warning(f"⚠️ O país '{nome}' já está cadastrado.")
                except Exception as e:
                    st.error(f"❌ Erro: {e}")

st.divider()

# -----------------------------------------
# LISTA DE PAÍSES
# -----------------------------------------
st.subheader("📋 Lista de Países Cadastrados")

try:
    df = pd.read_sql("SELECT * FROM paises ORDER BY id;", engine)

    if not df.empty:
        for _, row in df.iterrows():
            with st.container():
                c1, c2, c3 = st.columns([0.2, 0.6, 0.2])
                c1.markdown(f"**🆔 {row['id']}**")
                c2.markdown(f"**{row['nome']}**")
                if c3.button("🗑️ Excluir", key=f"del_{row['id']}"):
                    with engine.begin() as conn:
                        conn.execute(text("DELETE FROM paises WHERE id = :id"), {"id": row['id']})
                    st.success(f"🗑️ País '{row['nome']}' removido com sucesso!")
                    st.rerun()
    else:
        st.info("Nenhum país cadastrado ainda.")
except Exception as e:
    st.error(f"❌ Erro ao carregar países: {e}")

st.divider()

st.caption("💡 MindTrade © 2025 — Interface adaptada do modelo *Stock Peer Analysis* para o seu sistema de trading.")
