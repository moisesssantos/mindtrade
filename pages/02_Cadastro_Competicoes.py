import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

# -----------------------------------------
# CONFIGURAÇÃO GERAL
# -----------------------------------------
st.set_page_config(page_title="Cadastro de Competições", layout="wide", page_icon="🏆")

# Tema escuro visual
st.markdown("""
    <style>
        body {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .stApp { background-color: #0E1117; }
        h1, h2, h3 { color: #00C0F3; }
        .stButton > button {
            background-color: #00C0F3;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5em 1em;
            font-weight: bold;
            transition: 0.2s;
        }
        .stButton > button:hover {
            background-color: #008FB5;
            transform: scale(1.05);
        }
        .card {
            background-color: #1E222A;
            border-radius: 12px;
            padding: 10px;
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

st.title("🏆 Cadastro de Competições")
st.markdown("Gerencie as competições e relacione-as com seus países correspondentes.")

st.divider()

# -----------------------------------------
# CARREGAR PAÍSES
# -----------------------------------------
try:
    df_paises = pd.read_sql("SELECT id, nome FROM paises ORDER BY nome;", engine)
    lista_paises = df_paises["nome"].tolist()
    mapa_paises = dict(zip(df_paises["nome"], df_paises["id"]))
except Exception as e:
    st.error(f"Erro ao carregar países: {e}")
    lista_paises = []
    mapa_paises = {}

# -----------------------------------------
# ESTADO LOCAL (para edição)
# -----------------------------------------
if "edit_id" not in st.session_state:
    st.session_state.edit_id = ""
if "edit_nome" not in st.session_state:
    st.session_state.edit_nome = ""
if "edit_pais" not in st.session_state:
    st.session_state.edit_pais = ""

# -----------------------------------------
# FORMULÁRIO
# -----------------------------------------
st.subheader("➕ Adicionar / ✏️ Editar Competição")

with st.form("form_competicoes", clear_on_submit=False):
    nome = st.text_input("Nome da competição", value=st.session_state.edit_nome)
    pais_selecionado = st.selectbox(
        "País",
        lista_paises,
        index=lista_paises.index(st.session_state.edit_pais)
        if st.session_state.edit_pais in lista_paises else 0
    )
    enviar = st.form_submit_button("Salvar / Atualizar")

    if enviar:
        if nome.strip() == "":
            st.warning("⚠️ Informe o nome da competição.")
        else:
            try:
                with engine.begin() as conn:
                    if st.session_state.edit_id == "":
                        conn.execute(
                            text("INSERT INTO competicoes (nome, id_pais) VALUES (:nome, :id_pais)"),
                            {"nome": nome, "id_pais": mapa_paises[pais_selecionado]},
                        )
                        st.success(f"✅ Competição '{nome}' adicionada com sucesso!")
                    else:
                        conn.execute(
                            text("UPDATE competicoes SET nome = :nome, id_pais = :id_pais WHERE id = :id"),
                            {"nome": nome, "id_pais": mapa_paises[pais_selecionado], "id": st.session_state.edit_id},
                        )
                        st.success(f"✏️ Competição '{nome}' atualizada com sucesso!")

                    # limpar estado após salvar
                    st.session_state.edit_id = ""
                    st.session_state.edit_nome = ""
                    st.session_state.edit_pais = ""
                    st.rerun()

            except IntegrityError:
                st.warning(f"⚠️ A competição '{nome}' já está cadastrada nesse país.")
            except Exception as e:
                st.error(f"❌ Erro: {e}")

st.divider()

# -----------------------------------------
# LISTA DE COMPETIÇÕES
# -----------------------------------------
st.subheader("📋 Lista de Competições")

try:
    df = pd.read_sql("""
        SELECT c.id, c.nome AS competencia, p.nome AS pais
        FROM competicoes c
        JOIN paises p ON c.id_pais = p.id
        ORDER BY p.nome, c.nome;
    """, engine)

    if not df.empty:
        for _, row in df.iterrows():
            col1, col2, col3, col4, col5 = st.columns([0.5, 3, 2, 1, 1])
            col1.markdown(f"**{row['id']}**")
            col2.markdown(f"🏆 {row['competencia']}")
            col3.markdown(f"🌍 {row['pais']}")

            if col4.button("✏️ Editar", key=f"edit_{row['id']}"):
                st.session_state.edit_id = row["id"]
                st.session_state.edit_nome = row["competencia"]
                st.session_state.edit_pais = row["pais"]
                st.rerun()

            if col5.button("🗑️ Excluir", key=f"del_{row['id']}"):
                with engine.begin() as conn:
                    conn.execute(text("DELETE FROM competicoes WHERE id = :id"), {"id": row["id"]})
                st.success(f"🗑️ Competição '{row['competencia']}' excluída com sucesso!")
                st.rerun()
    else:
        st.info("Nenhuma competição cadastrada ainda.")
except Exception as e:
    st.error(f"❌ Erro ao carregar competições: {e}")
