import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

# -----------------------------------------
# CONFIGURAÇÃO INICIAL
# -----------------------------------------
st.set_page_config(page_title="Cadastro de Mercados", layout="wide", page_icon="💹")

# -----------------------------------------
# ESTILO VISUAL (Glassmorphism + Tema Claro)
# -----------------------------------------
st.markdown("""
    <style>
        /* Layout geral */
        body {
            background-color: #FFFFFF;
            color: #1C1C1C;
        }
        .stApp {
            background-color: #FFFFFF;
        }

        /* Títulos */
        h1, h2, h3 {
            color: #005B9F;
        }
        h1 {
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            margin-bottom: 0.6rem !important;
        }

        /* Botão principal (Salvar / Atualizar) */
        .stButton > button {
            background: rgba(0, 122, 204, 0.15) !important;
            color: #005A99 !important;
            border: 1px solid rgba(0, 122, 204, 0.4) !important;
            border-radius: 8px !important;
            padding: 0.5em 1em !important;
            font-weight: 600 !important;
            font-size: 0.9em !important;
            backdrop-filter: blur(4px);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
            transition: all 0.2s ease-in-out;
        }
        .stButton > button:hover {
            background: rgba(0, 122, 204, 0.25) !important;
            color: #004777 !important;
            transform: translateY(-1px);
        }

        /* Cartões */
        .card {
            background: rgba(250, 250, 250, 0.85);
            border-radius: 10px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
            padding: 1rem;
            margin-bottom: 10px;
            border: 1px solid #E5E5E5;
        }

        /* Botões pequenos da lista */
        div[data-testid="stButton"] > button[kind="secondary"],
        div[data-testid="stButton"] > button[kind="primary"] {
            padding: 0.3em 0.7em !important;
            font-size: 0.85em !important;
            border-radius: 6px !important;
            margin: 0 3px !important;
            font-weight: 600 !important;
            border: 1px solid rgba(0,0,0,0.1) !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        }

        /* Editar = Azul translúcido */
        div[data-testid="stButton"]:has(span:contains("Editar")) > button {
            background: rgba(0, 122, 204, 0.15) !important;
            color: #004777 !important;
        }
        div[data-testid="stButton"]:has(span:contains("Editar")) > button:hover {
            background: rgba(0, 122, 204, 0.25) !important;
        }

        /* Excluir = Vermelho translúcido */
        div[data-testid="stButton"]:has(span:contains("Excluir")) > button,
        div[data-testid="stButton"]:has(span:contains("Remover")) > button {
            background: rgba(217, 83, 79, 0.15) !important;
            color: #7A1412 !important;
        }
        div[data-testid="stButton"]:has(span:contains("Excluir")) > button:hover,
        div[data-testid="stButton"]:has(span:contains("Remover")) > button:hover {
            background: rgba(217, 83, 79, 0.25) !important;
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
# TÍTULO E DESCRIÇÃO
# -----------------------------------------
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
                col1, col2, col3, col4, col5 = st.columns([0.4, 3, 3, 0.8, 0.8])
                col1.markdown(f"**{row['id']}**")
                col2.markdown(f"💹 **{row['nome']}**")
                col3.markdown(f"{row['descricao'] if row['descricao'] else '—'}")

                if col4.button("✏️ Editar", key=f"edit_{row['id']}"):
                    st.session_state.edit_id = row["id"]
                    st.session_state.edit_nome = row["nome"]
                    st.session_state.edit_desc = row["descricao"] or ""
                    st.rerun()

                if col5.button("🗑️ Excluir", key=f"del_{row['id']}"):
                    with engine.connect() as conn:
                        conn.execute(text("DELETE FROM mercados WHERE id = :id"), {"id": row["id"]})
                        conn.commit()
                    st.success(f"🗑️ Mercado '{row['nome']}' removido com sucesso!")
                    st.rerun()
    else:
        st.info("Nenhum mercado cadastrado ainda.")
except Exception as e:
    st.error(f"❌ Erro ao carregar mercados: {e}")
