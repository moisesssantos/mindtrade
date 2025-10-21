import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

# -----------------------------------------
# CONFIGURAÇÃO INICIAL
# -----------------------------------------
st.set_page_config(page_title="Cadastro de Mercados", layout="wide", page_icon="💹")

# Tema claro estilo Seattle Weather com botões compactos e coloridos
st.markdown("""
    <style>
        /* Layout geral */
        body {
            background-color: #FAFAFA;
            color: #1C1C1C;
        }
        .stApp {
            background-color: #FAFAFA;
        }

        /* Títulos */
        h1, h2, h3 {
            color: #005B9F;
        }

        /* Botão padrão (como o de salvar no formulário) */
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

        /* Cartões e containers */
        .card {
            background-color: #FFFFFF;
            border-radius: 10px;
            box-shadow: 0px 1px 4px rgba(0,0,0,0.1);
            padding: 1rem;
            margin-bottom: 10px;
        }

        /* Botões pequenos para ações da lista (Editar / Excluir) */
        div[data-testid="stButton"] > button[kind="secondary"],
        div[data-testid="stButton"] > button[kind="primary"] {
            padding: 0.25em 0.6em;
            font-size: 0.85em;
            border-radius: 4px;
            margin: 0 3px;
            font-weight: 600;
        }

        /* Editar = Azul */
        div[data-testid="stButton"] > button:has(span:contains("Editar")) {
            background-color: #007ACC !important;
            color: white !important;
        }
        div[data-testid="stButton"] > button:has(span:contains("Editar")):hover {
            background-color: #005A99 !important;
        }

        /* Excluir = Vermelho */
        div[data-testid="stButton"] > button:has(span:contains("Excluir")),
        div[data-testid="stButton"] > button:has(span:contains("Remover")) {
            background-color: #D9534F !important;
            color: white !important;
        }
        div[data-testid="stButton"] > button:has(span:contains("Excluir")):hover,
        div[data-testid="stButton"] > button:has(span:contains("Remover")):hover {
            background-color: #B52B27 !important;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------
# CONEXÃO COM O BANCO
# -----------------------------------------
engine = create_engine(
    "postgresql://neondb_owner:npg_xdZKq5FRT8Wn@ep-dry-wind-adh6ysjv-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

st.title("💹 Cadastro de Mercados")
st.markdown("Gerencie os tipos de mercado usados nas estratégias do MindTrade.")

st.divider()

# -----------------------------------------
# ESTADO LOCAL (edição)
# -----------------------------------------
if "edit_id" not in st.session_state:
    st.session_state.edit_id = ""
if "edit_nome" not in st.session_state:
    st.session_state.edit_nome = ""
if "edit_desc" not in st.session_state:
    st.session_state.edit_desc = ""

# -----------------------------------------
# FORMULÁRIO
# -----------------------------------------
st.subheader("➕ Adicionar / ✏️ Editar Mercado")

with st.form("form_mercados", clear_on_submit=False):
    nome = st.text_input("Nome do mercado", value=st.session_state.edit_nome)
    descricao = st.text_area("Descrição (opcional)", value=st.session_state.edit_desc, height=80)
    enviar = st.form_submit_button("Salvar / Atualizar")

    if enviar:
        if nome.strip() == "":
            st.warning("⚠️ Informe o nome do mercado.")
        else:
            try:
                if st.session_state.edit_id == "":
                    with engine.connect() as conn:
                        conn.execute(
                            text("INSERT INTO mercados (nome, descricao) VALUES (:nome, :descricao)"),
                            {"nome": nome, "descricao": descricao},
                        )
                        conn.commit()
                    st.success(f"✅ Mercado '{nome}' adicionado com sucesso!")
                else:
                    with engine.connect() as conn:
                        conn.execute(
                            text("UPDATE mercados SET nome = :nome, descricao = :descricao WHERE id = :id"),
                            {"nome": nome, "descricao": descricao, "id": st.session_state.edit_id},
                        )
                        conn.commit()
                    st.success(f"✏️ Mercado '{nome}' atualizado com sucesso!")

                st.session_state.edit_id = ""
                st.session_state.edit_nome = ""
                st.session_state.edit_desc = ""
                st.rerun()

            except IntegrityError:
                st.warning(f"⚠️ O mercado '{nome}' já está cadastrado.")
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {e}")

st.divider()

# -----------------------------------------
# LISTA DE MERCADOS
# -----------------------------------------
st.subheader("📋 Lista de Mercados")

try:
    df = pd.read_sql("SELECT * FROM mercados ORDER BY nome;", engine)
    if not df.empty:
        for _, row in df.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([0.5, 3, 3, 1])
                col1.markdown(f"**{row['id']}**")
                col2.markdown(f"💹 **{row['nome']}**")
                col3.markdown(f"{row['descricao'] if row['descricao'] else '—'}")

                if col4.button("✏️ Editar", key=f"edit_{row['id']}"):
                    st.session_state.edit_id = row["id"]
                    st.session_state.edit_nome = row["nome"]
                    st.session_state.edit_desc = row["descricao"] or ""
                    st.rerun()

                if col4.button("🗑️ Excluir", key=f"del_{row['id']}"):
                    with engine.connect() as conn:
                        conn.execute(text("DELETE FROM mercados WHERE id = :id"), {"id": row["id"]})
                        conn.commit()
                    st.success(f"🗑️ Mercado '{row['nome']}' removido com sucesso!")
                    st.rerun()
    else:
        st.info("Nenhum mercado cadastrado ainda.")
except Exception as e:
    st.error(f"❌ Erro ao carregar mercados: {e}")
