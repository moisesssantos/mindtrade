import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

# -----------------------------------------
# CONFIGURAÇÃO INICIAL
# -----------------------------------------
st.set_page_config(page_title="Cadastro de Estratégias", layout="wide", page_icon="🎯")

# -----------------------------------------
# ESTILO VISUAL (Tema Claro + Botões translúcidos)
# -----------------------------------------
st.markdown("""
    <style>
        body {
            background-color: #FFFFFF;
            color: #1C1C1C;
        }
        .stApp {
            background-color: #FFFFFF;
        }
        h1, h2, h3 {
            color: #005B9F;
        }
        h1 {
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            margin-bottom: 0.6rem !important;
        }
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
        .card {
            background: rgba(250, 250, 250, 0.85);
            border-radius: 10px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
            padding: 1rem;
            margin-bottom: 10px;
            border: 1px solid #E5E5E5;
        }
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
        div[data-testid="stButton"]:has(span:contains("Editar")) > button {
            background: rgba(0, 122, 204, 0.15) !important;
            color: #004777 !important;
        }
        div[data-testid="stButton"]:has(span:contains("Editar")) > button:hover {
            background: rgba(0, 122, 204, 0.25) !important;
        }
        div[data-testid="stButton"]:has(span:contains("Excluir")) > button {
            background: rgba(217, 83, 79, 0.15) !important;
            color: #7A1412 !important;
        }
        div[data-testid="stButton"]:has(span:contains("Excluir")) > button:hover {
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
st.title("🎯 Cadastro de Estratégias")
st.markdown("Gerencie as estratégias de trading e associe cada uma a um mercado padrão.")

st.divider()

# -----------------------------------------
# CARREGAR MERCADOS
# -----------------------------------------
try:
    df_mercados = pd.read_sql("SELECT id, nome FROM mercados ORDER BY nome;", engine)
    lista_mercados = df_mercados["nome"].tolist()
    mapa_mercados = dict(zip(df_mercados["nome"], df_mercados["id"]))
except Exception as e:
    st.error(f"❌ Erro ao carregar mercados: {e}")
    lista_mercados = []
    mapa_mercados = {}

# -----------------------------------------
# ESTADO LOCAL
# -----------------------------------------
if "edit_id" not in st.session_state:
    st.session_state.edit_id = ""
if "edit_nome" not in st.session_state:
    st.session_state.edit_nome = ""
if "edit_desc" not in st.session_state:
    st.session_state.edit_desc = ""
if "edit_mercado" not in st.session_state:
    st.session_state.edit_mercado = ""

# -----------------------------------------
# FORMULÁRIO
# -----------------------------------------
st.subheader("➕ Adicionar / ✏️ Editar Estratégia")

with st.form("form_estrategias", clear_on_submit=False):
    nome = st.text_input("Nome da estratégia", value=st.session_state.edit_nome)
    descricao = st.text_area("Descrição (opcional)", value=st.session_state.edit_desc, height=80)
    mercado_sel = st.selectbox(
        "Mercado padrão",
        options=lista_mercados if lista_mercados else ["Nenhum mercado disponível"],
        index=lista_mercados.index(st.session_state.edit_mercado)
        if st.session_state.edit_mercado in lista_mercados else 0
    )
    enviar = st.form_submit_button("Salvar / Atualizar")

    if enviar:
        if not lista_mercados:
            st.error("❌ Nenhum mercado cadastrado. Cadastre um mercado primeiro.")
        elif nome.strip() == "":
            st.warning("⚠️ Informe o nome da estratégia.")
        else:
            try:
                id_mercado = mapa_mercados.get(mercado_sel)
                if not id_mercado:
                    st.error("❌ Mercado inválido.")
                else:
                    if st.session_state.edit_id == "":
                        with engine.connect() as conn:
                            conn.execute(
                                text("INSERT INTO estrategias (nome, descricao, id_mercado) VALUES (:nome, :descricao, :id_mercado)"),
                                {"nome": nome, "descricao": descricao, "id_mercado": id_mercado},
                            )
                            conn.commit()
                        st.success(f"✅ Estratégia '{nome}' adicionada com sucesso!")
                    else:
                        with engine.connect() as conn:
                            conn.execute(
                                text("UPDATE estrategias SET nome = :nome, descricao = :descricao, id_mercado = :id_mercado WHERE id = :id"),
                                {"nome": nome, "descricao": descricao, "id_mercado": id_mercado, "id": st.session_state.edit_id},
                            )
                            conn.commit()
                        st.success(f"✏️ Estratégia '{nome}' atualizada com sucesso!")

                    st.session_state.edit_id = ""
                    st.session_state.edit_nome = ""
                    st.session_state.edit_desc = ""
                    st.session_state.edit_mercado = ""
                    st.rerun()
            except IntegrityError:
                st.warning(f"⚠️ A estratégia '{nome}' já está cadastrada.")
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {e}")

st.divider()

# -----------------------------------------
# LISTA DE ESTRATÉGIAS
# -----------------------------------------
st.subheader("📋 Lista de Estratégias")

try:
    df = pd.read_sql("""
        SELECT e.id, e.nome AS estrategia, e.descricao, m.nome AS mercado
        FROM estrategias e
        LEFT JOIN mercados m ON e.id_mercado = m.id
        ORDER BY e.nome;
    """, engine)

    if not df.empty:
        for _, row in df.iterrows():
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns([0.4, 2.5, 3, 2, 0.8, 0.8])
                col1.markdown(f"**{row['id']}**")
                col2.markdown(f"🎯 **{row['estrategia']}**")
                col3.markdown(f"{row['descricao'] if row['descricao'] else '—'}")
                col4.markdown(f"💹 {row['mercado'] if row['mercado'] else '—'}")

                if col5.button("✏️ Editar", key=f"edit_{row['id']}"):
                    st.session_state.edit_id = row["id"]
                    st.session_state.edit_nome = row["estrategia"]
                    st.session_state.edit_desc = row["descricao"] or ""
                    st.session_state.edit_mercado = row["mercado"] or ""
                    st.rerun()

                if col6.button("🗑️ Excluir", key=f"del_{row['id']}"):
                    with engine.connect() as conn:
                        conn.execute(text("DELETE FROM estrategias WHERE id = :id"), {"id": row["id"]})
                        conn.commit()
                    st.success(f"🗑️ Estratégia '{row['estrategia']}' removida com sucesso!")
                    st.rerun()
    else:
        st.info("Nenhuma estratégia cadastrada ainda.")
except Exception as e:
    st.error(f"❌ Erro ao carregar estratégias: {e}")
