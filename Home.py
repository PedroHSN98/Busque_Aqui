import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import pydeck as pdk
from pathlib import Path
import base64

# =======================
# CONFIG DA PÁGINA
# =======================
st.set_page_config(page_title="Encontre aqui", layout="wide")

# Caminho da sua logo (ajuste se quiser outro local/nome)
LOGO_PATH = Path("assets/busque_aqui_logo.png")
# =======================
# CSS GLOBAL + POSIÇÃO DA LOGO
# =======================
st.markdown("""
    <style>
    .stApp { background-color: #0b0b3b; color: white; }
    h1, h2, h3, h4, h5, h6 { color: white; }

    .stButton>button {
        background-color: #C077F3; color: white; border-radius: 10px;
        padding: 10px 20px; border: none; font-weight: bold;
    }
    .stButton>button:hover { background-color: #A355E2; color: white; }

    .stSelectbox>div>div>div {
        appearance: none; background-color: white; color: black; border-radius: 10px;
    }
    div[data-baseweb="select"] svg {
       color: black !important; fill: black !important; width: 20px !important;
       height: 30px !important; visibility: visible !important; display: block !important;
    }
    .stTextInput>div>div>input {
        background-color: white; color: black; border: 2px solid #C077F3; border-radius: 10px;
    }

    /* LOGO fixa no canto superior esquerdo */
    .app-logo {
        position: fixed;
        top: 50px;
        left: 75x;
        width: 160px;        /* ajuste o tamanho aqui */
        height: auto;
        z-index: 9999;       /* fica por cima dos elementos */
        border-radius: 12px; /* opcional: cantos arredondados */
        box-shadow: 0 2px 10px rgba(0,0,0,0.25); /* opcional */
        pointer-events: none; /* não intercepta cliques da UI */
    }
    /* Espaço superior opcional se quiser evitar sobreposição do título
       .app-top-spacer { height: 80px; } */
    </style>
""", unsafe_allow_html=True)

# =======================
# RENDER DA LOGO (SEM SIDEBAR)
# =======================
def render_logo():
    if LOGO_PATH.exists():
        mime = "image/png" if LOGO_PATH.suffix.lower() == ".png" else "image/jpeg"
        data = LOGO_PATH.read_bytes()
        b64 = base64.b64encode(data).decode("utf-8")
        st.markdown(f'<img class="app-logo" src="data:{mime};base64,{b64}" alt="Busque Aqui logo" />',
                    unsafe_allow_html=True)
    else:
        # fallback discreto (sem imagem) — você só verá quando a logo não existir ainda
        st.markdown("<!-- logo não encontrada: coloque em assets/logo-busque-aqui.png -->", unsafe_allow_html=True)

render_logo()
# st.markdown('<div class="app-top-spacer"></div>', unsafe_allow_html=True)  # use se quiser empurrar o conteúdo pra baixo

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
# TELAS
# =======================
def tela_home():
    st.markdown("<h1 style='text-align: center;'>Encontre aqui</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: left;'>Encontre estabelecimentos do bairro desejado:</h3>", unsafe_allow_html=True)

    tipo = st.selectbox(
        "Escolha o tipo de estabelecimento:",
        ["", "Farmácias", "Mercados", "Lojas", "Hospitais", "Óticas", "Outros"],
        index=0
    )

    bairro = st.text_input("Digite o bairro:")

    _, col_buscar, _, col_historico, _ = st.columns([3, 1, 0.3, 1, 3])

    with col_buscar:
        buscar = st.button("Buscar")

    with col_historico:
        historico = st.button("Histórico")

    if buscar:
        if tipo != "" and bairro != "":
            st.session_state.tipo = tipo
            st.session_state.bairro = bairro
            st.session_state.pagina = "resultados"
            st.session_state.selecionado = None
            st.rerun()
        else:
            st.warning("Por favor, selecione o tipo de estabelecimento e digite o bairro.")

    if historico:
        st.markdown("##### Últimas buscas:")
        if st.session_state.historico:
            for busca in reversed(st.session_state.historico[-5:]):
                st.write(f"- {busca}")
        else:
            st.write("Nenhuma busca recente.")

def tela_resultados():
    st.markdown("<h2 style='text-align: center;'>Resultados da busca</h2>", unsafe_allow_html=True)

    estabelecimentos = [
        {"nome": "Mercado Municipal Miguel Sutil", "endereco": "Av. Generoso Ponce, 268, Centro, Cuiabá, MT, 78005-290", "lat": -15.5985, "lon": -56.0930, "categoria": "Mercados"},
        {"nome": "Mercado do Porto (Antônio Moisés Nadaf)", "endereco": "Bairro do Porto, Cuiabá, MT", "lat": -15.6100, "lon": -56.0800, "categoria": "Mercados"},
        {"nome": "Supermercado Curió – Loja Cidade Alta", "endereco": "Av. Jornalista Alves de Oliveira, 352, Cidade Alta, Cuiabá, MT", "lat": -15.5820, "lon": -56.1000, "categoria": "Mercados"},
        {"nome": "Supermercado Curió – Loja Goiabeiras", "endereco": "Av. São Sebastião, 06, Popular, Cuiabá, MT", "lat": -15.5835, "lon": -56.1300, "categoria": "Mercados"},
        {"nome": "Mercearia Vitória", "endereco": "Rua Cinquenta e Seis, 18, Pedra 90, Cuiabá, MT", "lat": -15.6690, "lon": -56.1200, "categoria": "Mercados"},
        {"nome": "Farmácia Dia a Dia", "endereco": "Av. Brasília, 146, Cuiabá, MT", "lat": -15.5960, "lon": -56.0990, "categoria": "Farmácias"},
        {"nome": "Farmácia Pague Menos (Centro Sul)", "endereco": "Av. Isaac Póvoas, 807, Centro Sul, Cuiabá, MT", "lat": -15.5955, "lon": -56.0925, "categoria": "Farmácias"},
        {"nome": "Tave Pharma Cuiabá (Manipulação)", "endereco": "Av. Presidente Marques, 54, Centro Sul, Cuiabá, MT", "lat": -15.6000, "lon": -56.0930, "categoria": "Farmácias"},
        {"nome": "Farmácia Criativa", "endereco": "Av. Presidente Getúlio Vargas, 1203, Centro Norte, Cuiabá, MT", "lat": -15.5760, "lon": -56.0860, "categoria": "Farmácias"},
        {"nome": "Farmácia Cuiabá", "endereco": "Av. Mario Palma, 760, Cuiabá, MT", "lat": -15.5800, "lon": -56.0900, "categoria": "Farmácias"},
        {"nome": "Ótica Vision", "endereco": "Rua das Lentes, 200, Cuiabá, MT", "lat": -15.6050, "lon": -56.1015, "categoria": "Óticas"},
        {"nome": "Loja Centro Fashion", "endereco": "Rua das Compras, 50, Cuiabá, MT", "lat": -15.5900, "lon": -56.0950, "categoria": "Lojas"}
    ]

    tipo = st.session_state.get("tipo", "")
    if tipo and tipo != "Outros":
        filtrados = [e for e in estabelecimentos if e["categoria"] == tipo]
    else:
        filtrados = estabelecimentos.copy()

    if st.session_state.selecionado and st.session_state.selecionado not in filtrados:
        st.session_state.selecionado = None

    st.markdown(f"##### Estabelecimentos encontrados ({tipo or 'Todos'}):")
    if not filtrados:
        st.info("Nenhum estabelecimento encontrado para o tipo selecionado.")
    else:
        for est in filtrados:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{est['nome']}** – {est['endereco']}")
            with col2:
                if st.button(f"Visitar {est['nome']}", key=f"visit_{est['nome']}"):
                    st.session_state.historico.append(f"{est['nome']} - {est['endereco']}")
                    st.session_state.selecionado = est
                    st.rerun()

    st.markdown("### 📍 Mapa interativo da região")
    if filtrados:
        df = pd.DataFrame(filtrados)
        layer_base = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position='[lon, lat]',
            get_fill_color='[0, 180, 0, 180]',
            get_radius=70,
            pickable=True
        )
        layers = [layer_base]

        if st.session_state.selecionado:
            df_sel = pd.DataFrame([st.session_state.selecionado])
            layer_sel = pdk.Layer(
                "ScatterplotLayer",
                data=df_sel,
                get_position='[lon, lat]',
                get_fill_color='[255, 0, 0, 255]',
                get_radius=35,
                pickable=True
            )
            layers.append(layer_sel)
            view_state = pdk.ViewState(
                latitude=float(st.session_state.selecionado["lat"]),
                longitude=float(st.session_state.selecionado["lon"]),
                zoom=16, pitch=0, bearing=0
            )
        else:
            view_state = pdk.ViewState(
                latitude=float(df["lat"].mean()),
                longitude=float(df["lon"].mean()),
                zoom=12.5, pitch=0, bearing=0
            )

        tooltip = {"text": "{nome}\n{endereco}"}
        deck = pdk.Deck(layers=layers, initial_view_state=view_state, map_style=None, tooltip=tooltip)
        st.pydeck_chart(deck)
    else:
        st.write("Sem dados para exibir no mapa.")

    if st.button("Voltar"):
        st.session_state.pagina = "home"
        st.session_state.selecionado = None

# =======================
# CONTROLADOR
# =======================
if st.session_state.pagina == "home":
    tela_home()
elif st.session_state.pagina == "resultados":
    tela_resultados()
