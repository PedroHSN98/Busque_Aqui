import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Encontre aqui", layout="wide")

# Estado da página
if "pagina" not in st.session_state:
    st.session_state.pagina = "home"

# Histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# Estilos personalizados
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0b3b;
        color: white;
    }
    h1, h2, h3, h4, h5, h6 {
        color: white;
    }
    .stButton>button {
        background-color: #C077F3;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #A355E2;
        color: white;
    }
    .stSelectbox>div>div>div {
        appearance: none;
        background-color: white;
        color: black;
        border-radius: 10px;
    }
    div[data-baseweb="select"] svg {
       color: black !important;
       fill: black !important;
       width: 20px !important;
       height: 30px !important;
       visibility: visible !important;
       display: block !important;
    }
    .stTextInput>div>div>input {
        background-color: white;
        color: black;
        border: 2px solid #C077F3;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# =======================
# TELA INICIAL
# =======================
def tela_home():
    st.markdown("<h1 style='text-align: center;'>Encontre aqui</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: left;'>Encontre estabelecimentos do bairro desejado:</h3>", unsafe_allow_html=True)

    tipo = st.selectbox("Escolha o tipo de estabelecimento:", ["Farmácias", "Mercados", "Lojas", "Hospitais", "Óticas", "Outros"])
    bairro = st.text_input("Digite o bairro:")

    espaco1, col_buscar, espaco_meio, col_historico, espaco2 = st.columns([3, 1, 0.3, 1, 3])

    with col_buscar:
        buscar = st.button("Buscar")

    with col_historico:
        historico = st.button("Histórico")

    # Lógica do botão Buscar
    if buscar:
        if bairro:
            st.session_state.tipo = tipo
            st.session_state.bairro = bairro
            st.session_state.historico.append(f"{tipo} - {bairro}")
            st.session_state.pagina = "resultados"
            st.rerun()  
        else:
            st.warning("Digite o bairro antes de buscar.")

    # Lógica do botão Histórico
    if historico:
        st.markdown("##### Últimas buscas:")
        if st.session_state.historico:
            for busca in reversed(st.session_state.historico[-5:]):
                st.write(f"- {busca}")
        else:
            st.write("Nenhuma busca recente.")

# =======================
# TELA DE RESULTADOS
# =======================
def tela_resultados():
    st.markdown("<h2 style='text-align: center;'>Resultados da busca</h2>", unsafe_allow_html=True)

    st.write(f"**Tipo:** {st.session_state.tipo}")
    st.write(f"**Bairro:** {st.session_state.bairro}")

    # Exemplo de dados geográficos (você vai trocar por dados reais depois)
    dados_mapa = pd.DataFrame({
        'latitude': [-15.601410, -15.602310, -15.603210],
        'longitude': [-56.097891, -56.098800, -56.099700]
    })
    st.success("Aqui serão exibidos os estabelecimentos encontrados.")

    st.map(dados_mapa)

    if st.button("Voltar"):
        st.session_state.pagina = "home"
        st.rerun()  # Força voltar para a tela inicial

# =======================
# CONTROLADOR DE TELAS
# =======================
if st.session_state.pagina == "home":
    tela_home()
elif st.session_state.pagina == "resultados":
    tela_resultados()

