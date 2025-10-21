import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

# -----------------------------------------
# CONFIGURAÇÃO INICIAL
# -----------------------------------------
st.set_page_config(page_title="Cadastro de Países", layout="wide", page_icon="🌍")

# Tema claro no estilo Seattle Weather
st.markdown("""
    <style>
        body {
            background-color: #FAFAFA;
            color: #1C1C1C;
        }
        .stApp {
            background-color: #FAFAFA;
        }
        h1, h2, h3 {
            color: #005B9F;
        }
        .stButton > button {
            background-color: #007ACC;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.5em 1em;
            font-weight: bold;
            transition: 0.2s;
        }
        .stButton > button:hover {
            background-color: #005A99;
            transform: scale(1.02);
        }
        .card {
            background-color: #FFFFFF;
            border-radius: 10px;
            box-shadow: 0px 1px 4px rgba(0,0,0,0.1);
            padding: 1rem;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------
# CONEXÃO COM O BANCO
# -----------------------------------------
engine = create_engine(
    "postgresql://neondb_owner:npg_xdZKq5FRT8Wn@ep-dry-wind-adh6ysjv-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

st.title("🌍 Cadastro de Países")
st.markdown("Gerencie os países disponíveis no sistema MindTrade.")

st.divider()

# -----------------------------------------
# ESTADO LOCAL (para edição)
# -----------------------------------------
if "edit_id" not in st.session_state:
    st.session_state.edit_id = ""
if "edit_nome" not in st.session_state:
    st.session_state.edit_nome = ""

# -----------------------------------------
# FORMULÁRIO
# -----------------------------------------
st.subheader("➕ Adicionar / ✏️ Editar País")

with st.form("form_paises", clear_on_submit=False):
    nome = st.text_input("Nome do país", value=st.session_state.edit_nome)
    enviar = st.form_submit_button("Salvar / Atualizar")

    if enviar:
        if nome.strip() == "":
            st.warning("⚠️ Informe o nome do país.")
        else:
            try:
                if st.session_state.edit_id == "":
                    with engine.connect() as conn:
                        conn.execute(text("INSERT INTO paises (nome) VALUES (:nome)"), {"nome": nome})
                        conn.commit()
                    st.success(f"✅ País '{nome}' adicionado com sucesso!")
                else:
                    with engine.connect() as conn:
                        conn.execute(
                            text("UPDATE paises SET nome = :nome WHERE id = :id"),
                            {"nome": nome, "id": st.session_state.edit_id},
                        )
                        conn.commit()
                    st.success(f"✏️ País '{nome}' atualizado com sucesso!")

                st.session_state.edit_id = ""
                st.session_state.edit_nome = ""
                st.rerun()

            except IntegrityError:
                st.warning(f"⚠️ O país '{nome}' já está cadastrado.")
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {e}")

st.divider()

# -----------------------------------------
# LISTA DE PAÍSES
# -----------------------------------------
st.subheader("📋 Lista de Países")

try:
    df = pd.read_sql("SELECT * FROM paises ORDER BY id;", engine)
    if not df.empty:
        for _, row in df.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([0.5, 3, 1, 1])
                col1.markdown(f"**{row['id']}**")
                col2.markdown(f"🌎 {row['nome']}")
                if col3.button("✏️ Editar", key=f"edit_{row['id']}"):
                    st.session_state.edit_id = row["id"]
                    st.session_state.edit_nome = row["nome"]
                    st.rerun()
                if col4.button("🗑️ Excluir", key=f"del_{row['id']}"):
                    with engine.connect() as conn:
                        conn.execute(text("DELETE FROM paises WHERE id = :id"), {"id": row["id"]})
                        conn.commit()
                    st.success(f"🗑️ País '{row['nome']}' removido com sucesso!")
                    st.rerun()
    else:
        st.info("Nenhum país cadastrado ainda.")
except Exception as e:
    st.error(f"❌ Erro ao carregar países: {e}")
