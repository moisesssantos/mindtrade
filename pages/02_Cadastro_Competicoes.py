import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

# -----------------------------------------
# CONFIGURAÇÃO INICIAL
# -----------------------------------------
st.set_page_config(page_title="Cadastro de Competições", layout="wide", page_icon="🏆")

# Tema claro estilo Seattle Weather
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

st.title("🏆 Cadastro de Competições")
st.markdown("Gerencie as competições e vincule-as aos países cadastrados.")

st.divider()

# -----------------------------------------
# CARREGAR PAÍSES
# -----------------------------------------
try:
    df_paises = pd.read_sql("SELECT id, nome FROM paises ORDER BY nome;", engine)
    lista_paises = df_paises["nome"].tolist()
    mapa_paises = dict(zip(df_paises["nome"], df_paises["id"]))
except Exception as e:
    st.error(f"❌ Erro ao carregar países: {e}")
    lista_paises = []
    mapa_paises = {}

# -----------------------------------------
# ESTADO LOCAL (edição)
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
        options=lista_paises if lista_paises else ["Nenhum país disponível"],
        index=lista_paises.index(st.session_state.edit_pais)
        if st.session_state.edit_pais in lista_paises else 0
    )
    enviar = st.form_submit_button("Salvar / Atualizar")

    if enviar:
        if not lista_paises:
            st.error("❌ Nenhum país cadastrado. Cadastre um país primeiro.")
        elif nome.strip() == "":
            st.warning("⚠️ Informe o nome da competição.")
        else:
            try:
                id_pais = mapa_paises.get(pais_selecionado)
                if not id_pais:
                    st.error("❌ País inválido. Atualize a página e tente novamente.")
                else:
                    if st.session_state.edit_id == "":
                        with engine.connect() as conn:
                            conn.execute(
                                text("INSERT INTO competicoes (nome, id_pais) VALUES (:nome, :id_pais)"),
                                {"nome": nome, "id_pais": id_pais},
                            )
                            conn.commit()
                        st.success(f"✅ Competição '{nome}' adicionada com sucesso!")
                    else:
                        with engine.connect() as conn:
                            conn.execute(
                                text("UPDATE competicoes SET nome = :nome, id_pais = :id_pais WHERE id = :id"),
                                {"nome": nome, "id_pais": id_pais, "id": st.session_state.edit_id},
                            )
                            conn.commit()
                        st.success(f"✏️ Competição '{nome}' atualizada com sucesso!")

                    # limpar campos e atualizar
                    st.session_state.edit_id = ""
                    st.session_state.edit_nome = ""
                    st.session_state.edit_pais = ""
                    st.rerun()

            except IntegrityError:
                st.warning(f"⚠️ A competição '{nome}' já está cadastrada nesse país.")
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {e}")

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
            with st.container():
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
                    with engine.connect() as conn:
                        conn.execute(text("DELETE FROM competicoes WHERE id = :id"), {"id": row["id"]})
                        conn.commit()
                    st.success(f"🗑️ Competição '{row['competencia']}' removida com sucesso!")
                    st.rerun()
    else:
        st.info("Nenhuma competição cadastrada ainda.")
except Exception as e:
    st.error(f"❌ Erro ao carregar competições: {e}")
