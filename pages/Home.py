import streamlit as st

# -----------------------------------------
# CONFIGURAÇÕES INICIAIS
# -----------------------------------------
st.set_page_config(
    page_title="MindTrade - Início",
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------
# ESTILO VISUAL
# -----------------------------------------
st.markdown("""
    <style>
        body {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .stApp {
            background-color: #0E1117;
            text-align: center;
        }
        h1, h2, h3 {
            color: #00C0F3;
            text-align: center;
        }
        .menu-card {
            background-color: #1E222A;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0px 0px 15px rgba(0,192,243,0.2);
            transition: 0.3s;
        }
        .menu-card:hover {
            transform: scale(1.03);
            box-shadow: 0px 0px 25px rgba(0,192,243,0.4);
        }
        .stButton > button {
            background-color: #00C0F3;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.7em 1.5em;
            font-size: 1.1em;
            font-weight: bold;
            margin-top: 15px;
            transition: 0.2s;
        }
        .stButton > button:hover {
            background-color: #008FB5;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------
# CONTEÚDO PRINCIPAL
# -----------------------------------------
st.title("💠 MindTrade")
st.subheader("Sistema Integrado de Trading e Análise Profissional")

st.markdown("#### Selecione uma das áreas abaixo para começar:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2382/2382461.png", width=80)
    st.markdown("### 🌍 Cadastro de Países")
    st.write("Gerencie os países que participam das competições.")
    if st.button("Acessar Cadastro"):
        st.switch_page("pages/01_Cadastro_Paises.py")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/1484/1484551.png", width=80)
    st.markdown("### 📊 Dashboard (Seattle Weather)")
    st.write("Acompanhe lucros, greens e reds com visual moderno.")
    if st.button("Abrir Dashboard"):
        st.switch_page("mindtrade_test.py")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/1284/1284838.png", width=80)
    st.markdown("### 🧠 Estratégias e Operações")
    st.write("(Em breve) Central de análises e estratégias automatizadas.")
    st.button("Em desenvolvimento", disabled=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("💡 MindTrade © 2025 — Sistema completo para traders profissionais.")
