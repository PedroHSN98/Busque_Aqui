import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from urllib.parse import quote

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

    # Selectbox com campo inicial vazio
    tipo = st.selectbox(
        "Escolha o tipo de estabelecimento:",
        ["", "Farmácias", "Mercados", "Lojas", "Hospitais", "Óticas", "Outros"],
        index=0
    )

    bairro = st.text_input("Digite o bairro:")

    # Layout dos botões
    espaco1, col_buscar, espaco_meio, col_historico, espaco2 = st.columns([3, 1, 0.3, 1, 3])

    with col_buscar:
        buscar = st.button("Buscar")

    with col_historico:
        historico = st.button("Histórico")

    # Lógica do botão Buscar
    if buscar:
        if tipo != "" and bairro != "":
            st.session_state.tipo = tipo
            st.session_state.bairro = bairro
            st.session_state.historico.append(f"{tipo} - {bairro}")
            st.session_state.pagina = "resultados"
            st.rerun()
        else:
            st.warning("Por favor, selecione o tipo de estabelecimento e digite o bairro.")

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

    # Simulando uma lista de estabelecimentos encontrados no banco
    estabelecimentos = [
        {"nome": "Farmácia Vida", "endereco": "Av. Central, 123"},
        {"nome": "Farmácia Bem Estar", "endereco": "Rua das Flores, 45"},
        {"nome": "Farmácia Popular", "endereco": "Praça da Saúde, 10"},
    ]

    st.markdown("##### Estabelecimentos encontrados:")

    for est in estabelecimentos:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{est['nome']}** – {est['endereco']}")
        with col2:
            if st.button(f"Visitar {est['nome']}", key=est["nome"]):
                st.session_state.historico.append(f"{est['nome']} - {est['endereco']}")
                st.success(f"Você escolheu visitar: {est['nome']}")

    #Mostrar mapa do Google
    endereco_busca = f"{st.session_state.bairro}"
    endereco_formatado = quote(endereco_busca)
    mapa_url = f"https://www.google.com/maps/embed/v1/search?key=SUA_CHAVE_API&q={endereco_formatado}"

    st.markdown("### 📍 Mapa da região")
    components.html(f"""
        <iframe
            width="100%"
            height="400"
            style="border:0"
            loading="lazy"
            allowfullscreen
            referrerpolicy="no-referrer-when-downgrade"
            src="{mapa_url}">
        </iframe>
    """, height=400)

    # Botão para voltar
    if st.button("Voltar"):
        st.session_state.pagina = "home"
# =======================
# CONTROLADOR DE TELAS
# =======================
if st.session_state.pagina == "home":
    tela_home()
elif st.session_state.pagina == "resultados":
    tela_resultados()