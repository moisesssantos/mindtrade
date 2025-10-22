import streamlit as st

# ------------------------------------------------------
# CONFIGURAÇÃO INICIAL
# ------------------------------------------------------
st.set_page_config(page_title="MindTrade", layout="wide", page_icon="💹")

# ------------------------------------------------------
# ESTILO VISUAL DO SIDEBAR
# ------------------------------------------------------
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;           /* fundo suave */
        border-right: 1px solid #E2E8F0;     /* linha discreta */
        padding-top: 1.5rem !important;
    }

    /* Títulos das seções */
    .sidebar-content h3, .sidebar-content h2 {
        color: #005B9F !important;
        margin-top: 1rem !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
    }

    /* Links do menu */
    [data-testid="stSidebarNav"] a, .stSidebar a, div[data-testid="stSidebar"] a {
        font-weight: 600;
        color: #1E293B !important;
        padding: 4px 0px 4px 2px !important;
        display: block;
        text-decoration: none !important;
    }

    /* Efeito hover */
    div[data-testid="stSidebar"] a:hover {
        color: #005B9F !important;
        background-color: rgba(0,91,159,0.08);
        border-radius: 4px;
    }

    /* Divisores */
    .stSidebar hr {
        border: 0;
        border-top: 1px solid #E2E8F0;
        margin: 0.8rem 0;
    }

    /* Rodapé fixo */
    .sidebar-footer {
        font-size: 0.8rem;
        color: #64748B;
        text-align: center;
        margin-top: 2rem;
        position: fixed;
        bottom: 10px;
        left: 15px;
        width: 240px;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# CABEÇALHO DO MENU LATERAL
# ------------------------------------------------------
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/1484/1484551.png",  # pode trocar por um logo seu
    width=56,
)
st.sidebar.markdown("<h2 style='margin:0; color:#005B9F;'>MindTrade</h2>", unsafe_allow_html=True)
st.sidebar.caption("Sistema de operações e análise")
st.sidebar.markdown("---")

# ------------------------------------------------------
# NAVEGAÇÃO LATERAL (usa os arquivos da pasta pages/)
# ------------------------------------------------------
st.sidebar.markdown("### ⚙️ Cadastros")
st.sidebar.page_link("pages/01_Cadastro_Paises.py", label="🌎 Países")
st.sidebar.page_link("pages/02_Cadastro_Competicoes.py", label="🏆 Competições")
st.sidebar.page_link("pages/03_Cadastro_Equipes.py", label="⚽ Equipes")
st.sidebar.page_link("pages/04_Cadastro_Mercados.py", label="💹 Mercados")
st.sidebar.page_link("pages/05_Cadastro_Estrategias.py", label="🎯 Estratégias")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎬 Operações")
st.sidebar.page_link("pages/06_PreAnalise.py", label="📊 Pré-Análise")
st.sidebar.page_link("pages/07_Entradas.py", label="💼 Entradas")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Relatórios e Estatísticas")
st.sidebar.page_link("pages/08_Relatorios.py", label="📊 Relatórios Gerais")

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
Use o menu lateral para navegar entre os módulos de **cadastro**, **operação** e **análise**.
""")

st.info("👉 Dica: comece cadastrando **Países, Competições e Equipes** antes de criar suas estratégias.")
