import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

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
# FORMULÁRIO DE CADASTRO / EDIÇÃO
# -----------------------------------------
with st.form("form_paises"):
    nome = st.text_input("Nome do país")
    id_editar = st.text_input("ID (para editar um país existente)", "")
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

# -----------------------------------------
# LISTA E EXCLUSÃO
# -----------------------------------------
st.divider()
st.subheader("📋 Lista de Países Cadastrados")

try:
    df = pd.read_sql("SELECT * FROM paises ORDER BY id;", engine)
    if not df.empty:
        for index, row in df.iterrows():
            col1, col2, col3 = st.columns([1, 4, 1])
            col1.write(f"**{row['id']}**")
            col2.write(row['nome'])
            if col3.button("🗑️ Excluir", key=f"del_{row['id']}"):
                with engine.begin() as conn:
                    conn.execute(text("DELETE FROM paises WHERE id = :id"), {"id": row['id']})
                st.success(f"🗑️ País '{row['nome']}' removido com sucesso!")
                st.rerun()
    else:
        st.info("Nenhum país cadastrado ainda.")
except Exception as e:
    st.error(f"❌ Erro ao carregar países: {e}")
