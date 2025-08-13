import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

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

    # Simulando estabelecimentos com coordenadas para o mapa
    estabelecimentos = [
        {
            "nome": "Mercado Municipal Miguel Sutil",
            "endereco": "Av. Generoso Ponce, 268, Centro, Cuiabá, MT, 78005-290",
            "lat": -15.5985,
            "lon": -56.0930
        },
        {
            "nome": "Mercado do Porto (Antônio Moisés Nadaf)",
            "endereco": "Bairro do Porto, Cuiabá, MT",
            "lat": -15.6100,
            "lon": -56.0800
        },
        {
            "nome": "Supermercado Curió – Loja Cidade Alta",
            "endereco": "Av. Jornalista Alves de Oliveira, 352, Cidade Alta, Cuiabá, MT",
            "lat": -15.5820,
            "lon": -56.1000
        },
        {
            "nome": "Supermercado Curió – Loja Goiabeiras",
            "endereco": "Av. São Sebastião, 06, Popular, Cuiabá, MT",
            "lat": -15.5835,
            "lon": -56.1300
        },
        {
            "nome": "Mercearia Vitória",
            "endereco": "Rua Cinquenta e Seis, 18, Pedra 90, Cuiabá, MT",
            "lat": -15.6690,
            "lon": -56.1200
        },
        {
            "nome": "Farmácia Dia a Dia",
            "endereco": "Av. Brasília, 146, Cuiabá, MT",
            "lat": -15.5960,
            "lon": -56.0990
        },
        {
            "nome": "Farmácia Pague Menos (Centro Sul)",
            "endereco": "Av. Isaac Póvoas, 807, Centro Sul, Cuiabá, MT",
            "lat": -15.5955,
            "lon": -56.0925
        },
        {
            "nome": "Tave Pharma Cuiabá (Manipulação)",
            "endereco": "Av. Presidente Marques, 54, Centro Sul, Cuiabá, MT",
            "lat": -15.6000,
            "lon": -56.0930
        },
        {
            "nome": "Farmácia Criativa",
            "endereco": "Av. Presidente Getúlio Vargas, 1203, Centro Norte, Cuiabá, MT",
            "lat": -15.5760,
            "lon": -56.0860
        },
        {
            "nome": "Farmácia Cuiabá",
            "endereco": "Av. Mario Palma, 760, Cuiabá, MT",
            "lat": -15.5800,
            "lon": -56.0900
        }
    ]

    st.markdown("##### Estabelecimentos encontrados:")

    for est in estabelecimentos:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{est['nome']}** – {est['endereco']}")
        with col2:
            if st.button(f"Visitar {est['nome']}", key=est["nome"]):
                st.session_state.historico.append(f"{est['nome']} - {est['endereco']}")

    # Preparar dados para o mapa interativo
    df = pd.DataFrame(estabelecimentos)

    st.markdown("### 📍 Mapa interativo da região")
    st.map(df[['lat', 'lon']])

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