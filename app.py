import streamlit as st
from ui.home import tela_home
from ui.resultados import tela_resultados
from ui.logo import render_logo
from ui.style import inject_global_css



# =======================
# CONFIG DA PÁGINA
# =======================
st.set_page_config(page_title="Encontre aqui", layout="wide")

# =======================
# CSS + LOGO
# =======================
inject_global_css()
render_logo()

# =======================
# ESTADOS
# =======================
if "pagina" not in st.session_state:
    st.session_state.pagina = "home"
if "historico" not in st.session_state:
    st.session_state.historico = []
if "selecionado" not in st.session_state:
    st.session_state.selecionado = None

# =======================
# CONTROLADOR DE TELAS
# =======================
if st.session_state.pagina == "home":
    tela_home()
elif st.session_state.pagina == "resultados":
    tela_resultados()