import streamlit as st

# ------------------------------------------------------
# CONFIGURAÇÃO INICIAL
# ------------------------------------------------------
st.set_page_config(page_title="MindTrade", layout="wide", page_icon="💹")

# --- OCULTAR MENU PADRÃO DO STREAMLIT ---
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# ESTILO VISUAL DO SIDEBAR
# ------------------------------------------------------
st.markdown("""
<style>
    /* Fundo e estrutura geral da barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #E6CFF2;           /* fundo lilás */
        border-right: 1px solid #CDB4DB;
        padding-top: 1.2rem !important;
        width: 250px !important;
    }

    /* Títulos das seções */
    .sidebar-content h3, .sidebar-content h2 {
        color: #4B0082 !important;           /* mesma cor de MindTrade */
        margin-top: 0.6rem !important;
        margin-bottom: 0.3rem !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px;
    }

    /* Links do menu */
    .stSidebar a, div[data-testid="stSidebar"] a {
        font-weight: 600;
        color: #4B0082 !important;           /* mesma cor de MindTrade */
        display: block;
        padding: 2px 4px 2px 4px !important;
        margin: 1px 0 !important;
        text-decoration: none !important;
        border-radius: 4px;
        transition: background-color 0.2s ease, color 0.2s ease;
        font-size: 0.9rem !important;
    }

    /* Hover (passar o mouse) */
    div[data-testid="stSidebar"] a:hover {
        background-color: rgba(75, 0, 130, 0.1);
        color: #4B0082 !important;
    }

    /* Indicador da página ativa */
    div[data-testid="stSidebar"] a[data-testid="stPageLink-true"] {
        background-color: rgba(75, 0, 130, 0.18);
        color: #4B0082 !important;
        font-weight: 700 !important;
        border-left: 4px solid #4B0082;
        padding-left: 6px !important;
    }

    /* Divisores */
    .stSidebar hr {
        border: 0;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    }

    /* Rodapé fixo */
    .sidebar-footer {
        font-size: 0.8rem;
        color: #3C3C4A;
        text-align: center;
        margin-top: 1.8rem;
        position: fixed;
        bottom: 10px;
        left: 15px;
        width: 230px;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# CABEÇALHO DO MENU LATERAL
# ------------------------------------------------------
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/1484/1484551.png",
    width=52,
)
st.sidebar.markdown("<h2 style='margin:0; color:#4B0082;'>MindTrade</h2>", unsafe_allow_html=True)
st.sidebar.caption("Sistema de operações e análise")
st.sidebar.markdown("---")

# ------------------------------------------------------
# NAVEGAÇÃO LATERAL (ORDENADA POR USO)
# ------------------------------------------------------
st.sidebar.markdown("### 🎬 Operações")
st.sidebar.page_link("pages/06_PreAnalise.py", label="📊 Pré-Análise")
st.sidebar.page_link("pages/07_Entradas.py", label="💼 Entradas")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Relatórios")
st.sidebar.page_link("pages/08_Relatorios.py", label="📊 Relatórios Gerais")

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Cadastros")
st.sidebar.page_link("pages/01_Cadastro_Paises.py", label="🌎 Países")
st.sidebar.page_link("pages/02_Cadastro_Competicoes.py", label="🏆 Competições")
st.sidebar.page_link("pages/03_Cadastro_Equipes.py", label="⚽ Equipes")
st.sidebar.page_link("pages/04_Cadastro_Mercados.py", label="💹 Mercados")
st.sidebar.page_link("pages/05_Cadastro_Estrategias.py", label="🎯 Estratégias")

# ------------------------------------------------------
# RODAPÉ FIXO
# ------------------------------------------------------
st.sidebar.markdown(
    "<div class='sidebar-footer'>Versão 1.0 • © MindTrade<br>Desenvolvido por Moisés Santos</div>",
    unsafe_allow_html=True
)

# ------------------------------------------------------
# CONTEÚDO PRINCIPAL DA HOME
# ------------------------------------------------------
st.title("💹 Painel MindTrade")
st.markdown("""
Bem-vindo ao **MindTrade**, sua plataforma integrada de análise e controle de trading esportivo.  
Use o menu lateral para navegar entre os módulos de **operação**, **relatórios** e **cadastro**.
""")

st.info("👉 Dica: comece cadastrando **Países, Competições e Equipes** antes de criar suas estratégias.")
