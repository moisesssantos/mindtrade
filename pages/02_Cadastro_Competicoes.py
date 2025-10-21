import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

# -----------------------------------------
# CONFIGURAÇÕES INICIAIS
# -----------------------------------------
st.set_page_config(page_title="Cadastro de Competições", layout="wide", page_icon="🏆")

# Conexão com o banco
engine = create_engine(
    "postgresql://neondb_owner:npg_xdZKq5FRT8Wn@ep-dry-wind-adh6ysjv-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

st.title("🏆 Cadastro de Competições")

st.markdown("Gerencie as competições e vincule-as aos países cadastrados.")

st.divider()

# -----------------------------------------
# LISTA DE PAÍSES PARA SELEÇÃO
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
# FORMULÁRIO DE CADASTRO / EDIÇÃO
# -----------------------------------------
with st.form("form_competicoes"):
    nome = st.text_input("Nome da competição")
    pais_selecionado = st.selectbox("País", lista_paises)
    id_editar = st.text_input("ID (para editar uma competição existente)", "")
    enviar = st.form_submit_button("Salvar / Atualizar")

    if enviar:
        if nome.strip() == "" or pais_selecionado.strip() == "":
            st.warning("⚠️ Preencha todos os campos antes de salvar.")
        else:
            try:
                with engine.begin() as conn:
                    if id_editar.strip() == "":
                        conn.execute(
                            text("INSERT INTO competicoes (nome, id_pais) VALUES (:nome, :id_pais)"),
                            {"nome": nome, "id_pais": mapa_paises[pais_selecionado]},
                        )
                        st.success(f"✅ Competição '{nome}' adicionada com sucesso!")
                    else:
                        conn.execute(
                            text("UPDATE competicoes SET nome = :nome, id_pais = :id_pais WHERE id = :id"),
                            {"nome": nome, "id_pais": mapa_paises[pais_selecionado], "id": id_editar},
                        )
                        st.success(f"✏️ Competição ID {id_editar} atualizada para '{nome}'!")
            except IntegrityError:
                st.warning(f"⚠️ A competição '{nome}' já está cadastrada.")
            except Exception as e:
                st.error(f"❌ Erro ao inserir/atualizar: {e}")

st.divider()

# -----------------------------------------
# LISTAGEM E EXCLUSÃO
# -----------------------------------------
st.subheader("📋 Lista de Competições Cadastradas")

try:
    df = pd.read_sql("""
        SELECT c.id, c.nome AS competencia, p.nome AS pais
        FROM competicoes c
        JOIN paises p ON c.id_pais = p.id
        ORDER BY p.nome, c.nome;
    """, engine)

    if not df.empty:
        for _, row in df.iterrows():
            col1, col2, col3, col4 = st.columns([0.5, 2, 2, 1])
            col1.write(f"**{row['id']}**")
            col2.write(row["competencia"])
            col3.write(f"🌍 {row['pais']}")
            if col4.button("🗑️ Excluir", key=f"del_{row['id']}"):
                with engine.begin() as conn:
                    conn.execute(text("DELETE FROM competicoes WHERE id = :id"), {"id": row["id"]})
                st.success(f"🗑️ Competição '{row['competencia']}' removida com sucesso!")
                st.rerun()
    else:
        st.info("Nenhuma competição cadastrada ainda.")
except Exception as e:
    st.error(f"❌ Erro ao carregar competições: {e}")
