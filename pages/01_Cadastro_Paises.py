import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

st.set_page_config(page_title="Cadastro de Países", layout="wide", page_icon="🌍")

engine = create_engine(
    "postgresql://neondb_owner:npg_xdZKq5FRT8Wn@ep-dry-wind-adh6ysjv-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

st.title("🌍 Cadastro de Países")

with st.form("form_paises"):
    nome = st.text_input("Nome do país")
    id_editar = st.text_input("ID (para editar país existente)", "")
    enviar = st.form_submit_button("Salvar / Atualizar")

    if enviar:
    if nome.strip() == "":
        st.warning("⚠️ Informe o nome da competição.")
    elif pais_selecionado not in mapa_paises:
        st.error("❌ País inválido. Atualize a página e tente novamente.")
    else:
        try:
            with engine.begin() as conn:
                id_pais = mapa_paises[pais_selecionado]

                if st.session_state.edit_id == "":
                    conn.execute(
                        text("INSERT INTO competicoes (nome, id_pais) VALUES (:nome, :id_pais)"),
                        {"nome": nome, "id_pais": id_pais},
                    )
                    st.success(f"✅ Competição '{nome}' adicionada com sucesso!")
                else:
                    conn.execute(
                        text("UPDATE competicoes SET nome = :nome, id_pais = :id_pais WHERE id = :id"),
                        {"nome": nome, "id_pais": id_pais, "id": st.session_state.edit_id},
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
            st.error(f"❌ Erro ao salvar: {e}")

st.divider()
st.subheader("📋 Lista de Países Cadastrados")

try:
    df = pd.read_sql("SELECT * FROM paises ORDER BY id;", engine)
    if not df.empty:
        for _, row in df.iterrows():
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
