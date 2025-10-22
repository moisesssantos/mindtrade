import streamlit as st

# ------------------------------------------------------
# CONFIGURAÇÃO INICIAL
# ------------------------------------------------------
st.set_page_config(page_title="MindTrade", layout="wide", page_icon="💹")

# --- OCULTAR MENU PADRÃO DO STREAMLIT ---
st.markdown("""
    <style>
        /* Remove o menu lateral padrão */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        /* Remove o menu superior "Streamlit" */
        header {visibility: hidden;}
        /* Remove o rodapé padrão */
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
        background-color: #E6CFF2;           /* cor personalizada */
        border-right: 1px solid #CDB4DB;     /* borda mais suave */
        padding-top: 1.2rem !important;
        width: 250px !important;
    }

    /* Títulos das seções */
    .sidebar-content h3, .sidebar-content h2 {
        color: #4B0082 !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.3rem !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px;
    }

    /* Links do menu */
    .stSidebar a, div[data-testid="stSidebar"] a {
        font-weight: 600;
        color: #1E1E2F !important;
        display: block;
        padding: 2px 4px 2px 4px !important;
        margin: 2px 0 !important;
        text-decoration: none !important;
        border-radius: 4px;
        transition: background-color 0.2s ease, color 0.2s ease;
        font-size: 0.9rem !important;
    }

    /* Hover (passar o mouse) */
    div[data-testid="stSidebar"] a:hover {
        background-color: rgba(0, 91, 159, 0.1);
        color: #003366 !important;
    }

    /* Indicador da página ativa */
    div[data-testid="stSidebar"] a[data-testid="stPageLink-true"] {
        background-color: rgba(0, 91, 159, 0.15);
        color: #003366 !important;
        font-weight: 700 !important;
        border-left: 4px solid #005B9F;
        padding-left: 6px !important;
    }

    /* Divisores */
    .stSidebar hr {
        border: 0;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
        margin: 0.6rem 0;
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
    "https://cdn-icons-png.flaticon.com/512/1484/1484551.png",  # pode trocar por um logo seu
    width=52,
)
st.sidebar.markdown("<h2 style='margin:0; color:#4B0082;'>MindTrade</h2>", unsafe_allow_html=True)
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
