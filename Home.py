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
        left: 75px;
        width: 160px;
        height: auto;
        z-index: 9999;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.25);
        pointer-events: none;
    }
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
        st.markdown(
            f'<img class="app-logo" src="data:{mime};base64,{b64}" alt="Busque Aqui logo" />',
            unsafe_allow_html=True
        )
render_logo()

# =======================
# ESTADOS
# =======================
if "pagina" not in st.session_state:
    st.session_state.pagina = "home"

# cada item do histórico é um dict: {nome,endereco,lat,lon,categoria}
if "historico" not in st.session_state:
    st.session_state.historico = []

if "selecionado" not in st.session_state:
    st.session_state.selecionado = None

# =======================
# DADOS
# =======================
ESTABELECIMENTOS = [

    {"nome": "Farmácia Pague Menos", "endereco": "Av. Pres. Getúlio Vargas, 1039 - Goiabeiras, Cuiabá - MT, 78032-000", "lat": -15.59297, "lon": -56.10261, "categoria": "Farmácias"},
    {"nome": "Droga Geral", "endereco": "Praça 8 de Abril, 84 - Quilombo, Cuiabá - MT, 78158-620", "lat": -15.59052, "lon": -56.10688, "categoria": "Farmácias"},
    {"nome": "Drogaria São Bento", "endereco": "Av. Presidente Getúlio Vargas, 296 - Centro, Cuiabá - MT, 78005-370", "lat": -15.5986, "lon": -56.0790, "categoria": "Farmácias"},
    {"nome": "Farmácia CriAtiva", "endereco": "Av. Presidente Getúlio Vargas, 1203 - Centro, Cuiabá - MT, 78005-370", "lat": -15.5980, "lon": -56.0780, "categoria": "Farmácias"},
    {"nome": "Farmácia Moderna", "endereco": "Av. Isaac Póvoas, 1279 - Goiabeiras, Cuiabá - MT, 78045-440", "lat": -15.6060, "lon": -56.0930, "categoria": "Farmácias"},
    {"nome": "Drogaria São Bento", "endereco": "Av. Presidente Getúlio Vargas, 296 - Centro, Cuiabá - MT, 78005-370", "lat": -15.5986, "lon": -56.0789, "categoria": "Lojas"},
    {"nome": "Track & Field (Goiabeiras Shopping)", "endereco": "Av. José Monteiro de Figueiredo, 500 - Duque de Caxias, Cuiabá - MT, 78043-300", "lat": -15.5840, "lon": -56.1145, "categoria": "Lojas"},
    {"nome": "Loja 7 Cuiabá", "endereco": "Rua 13 de Junho, 533 - Centro, Cuiabá - MT", "lat": -15.5992, "lon": -56.0928, "categoria": "Lojas"},
    {"nome": "Kalunga (Pantanal Shopping)", "endereco": "Av. Historiador Rubens de Mendonça (Av. CPA), 3300 - Jardim Aclimação I, Cuiabá - MT, 78050-250", "lat": -15.6200, "lon": -56.0850, "categoria": "Lojas"},
    {"nome": "Gil Modas", "endereco": "Av. Gov. Dante Martins de Oliveira, 1137 - Novo Horizonte, Cuiabá - MT", "lat": -15.6205, "lon": -56.1032, "categoria": "Lojas"},
    {"nome": "Complexo Hospitalar de Cuiabá", "endereco": "Av. das Flores, 843, Jardim Cuiabá, Cuiabá, MT", "lat": -15.5985, "lon": -56.1285, "categoria": "Hospitais"},
    {"nome": "Hospital Amecor", "endereco": "Av. Historiador Rubens de Mendonça, 898, Baú, Cuiabá, MT, 78008-000", "lat": -15.59028, "lon": -56.08726, "categoria": "Hospitais"},
    {"nome": "Hospital Geral e Maternidade de Cuiabá", "endereco": "Rua 13 de Junho, 2101, Centro Norte, Cuiabá, MT, 78020-840", "lat": -15.5988, "lon": -56.0910, "categoria": "Hospitais"},
    {"nome": "Hospital São Mateus", "endereco": "Av. Aclimação, 335, Bosque da Saúde, Cuiabá, MT, 78050-040", "lat": -15.6100, "lon": -56.0920, "categoria": "Hospitais"},
    {"nome": "Hospital Santa Rosa", "endereco": "Av. Aclimação, 385, Jardim Santa Marta, Cuiabá, MT, 78050-050", "lat": -15.6095, "lon": -56.0918, "categoria": "Hospitais"},
    {"nome": "Óptica Central", "endereco": "Rua Antônio Maria, 343 - Centro, Cuiabá - MT", "lat": -15.5967, "lon": -56.0939, "categoria": "Óticas"},
    {"nome": "Ótica Tropical", "endereco": "Rua Miranda Reis, 280 - Poção, Cuiabá - MT", "lat": -15.6172, "lon": -56.1304, "categoria": "Óticas"},
    {"nome": "Vila dos Óculos", "endereco": "Rua Buenos Aires, 551 - Jardim das Américas, Cuiabá - MT", "lat": -15.6290, "lon": -56.0785, "categoria": "Óticas"},
    {"nome": "Ótica Clara", "endereco": "Rua Cândido Mariano, 431 - Centro, Cuiabá - MT", "lat": -15.5982, "lon": -56.0902, "categoria": "Óticas"},
    {"nome": "Óticas Diniz", "endereco": "Rua Cândido Mariano, 509 - Centro, Cuiabá - MT", "lat": -15.5977, "lon": -56.0895, "categoria": "Óticas"},{"nome": "Mercado Municipal Miguel Sutil", "endereco": "Av. Generoso Ponce, 268 - Centro, Cuiabá - MT, 78005-290", "lat": -15.5985, "lon": -56.0930, "categoria": "Mercados"},
    {"nome": "Comper Miguel Sutil", "endereco": "Av. Miguel Sutil, 10995 - Duque de Caxias, Cuiabá - MT, 78043-750", "lat": -15.5872, "lon": -56.0911, "categoria": "Mercados"},
    {"nome": "Fort Atacadista", "endereco": "Av. Fernando Corrêa da Costa, 1260 - Jardim Petrópolis, Cuiabá - MT, 78070-000", "lat": -15.6249, "lon": -56.0774, "categoria": "Mercados"},
    {"nome": "Supermercado Big Lar", "endereco": "Av. Historiador Rubens de Mendonça, 9320 - Ribeirão do Lipa, Cuiabá - MT, 78050-000", "lat": -15.5725, "lon": -56.0968, "categoria": "Mercados"},
    {"nome": "Supermercado América", "endereco": "Av. das Torres, 1655 - Jardim Imperial II, Cuiabá - MT, 78075-580", "lat": -15.5707, "lon": -56.0859, "categoria": "Mercados"},


]

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

    _, col_buscar, _, _, _ = st.columns([3, 1, 0.3, 1, 3])
    with col_buscar:
        buscar = st.button("Buscar")

    if buscar:
        if tipo != "" and bairro != "":
            st.session_state.tipo = tipo
            st.session_state.bairro = bairro
            st.session_state.pagina = "resultados"
            st.session_state.selecionado = None
            st.rerun()
        else:
            st.warning("Por favor, selecione o tipo de estabelecimento e digite o bairro.")

    # -------- Histórico com toggle (evita nested expanders)
    show_hist = st.toggle("Mostrar histórico (últimas 5 buscas)", value=False)
    if show_hist:
        ultimos = list(reversed(st.session_state.historico[-5:]))
        if not ultimos:
            st.write("Nenhuma busca recente.")
        else:
            for i, item in enumerate(ultimos):
                # suporte a histórico antigo que possa ter sido salvo como string
                if isinstance(item, str):
                    st.write(f"- {item}")
                    continue

                col1, col2, col3 = st.columns([6, 2, 2])
                with col1:
                    st.write(f"*{item['nome']}* – {item['endereco']} ({item['categoria']})")
                with col2:
                    if st.button("Mostrar no mapa", key=f"hist_show_{i}"):
                        st.session_state.tipo = item.get("categoria", "Outros")
                        st.session_state.selecionado = item
                        st.session_state.pagina = "resultados"
                        st.rerun()
                with col3:
                    maps_url = f"https://www.google.com/maps?q={item['lat']},{item['lon']}"
                    st.link_button("Abrir no Google Maps", maps_url)  # sem key

def tela_resultados():
    st.markdown("<h2 style='text-align: center;'>Resultados da busca</h2>", unsafe_allow_html=True)

    tipo = st.session_state.get("tipo", "")
    if tipo and tipo != "Outros":
        filtrados = [e for e in ESTABELECIMENTOS if e["categoria"] == tipo]
    else:
        filtrados = ESTABELECIMENTOS.copy()

    # Garante que o selecionado também apareça na lista (se não estiver no filtro atual)
    sel = st.session_state.get("selecionado")
    if sel:
        presente = any(
            (abs(e["lat"] - sel["lat"]) < 1e-9 and abs(e["lon"] - sel["lon"]) < 1e-9)
            or (e["nome"] == sel["nome"] and e["endereco"] == sel["endereco"])
            for e in filtrados
        )
        if not presente:
            filtrados = filtrados + [sel]

    st.markdown(f"##### Estabelecimentos encontrados ({tipo or 'Todos'}):")
    if not filtrados:
        st.info("Nenhum estabelecimento encontrado para o tipo selecionado.")
    else:
        for est in filtrados:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"*{est['nome']}* – {est['endereco']}")
            with col2:
                # Chave única usando nome + endereço + categoria
                btn_key = f"visit_{est['nome']}_{est['endereco']}_{est['categoria']}"
                if st.button(f"Visitar {est['nome']}", key=btn_key):
                    st.session_state.historico.append({
                        "nome": est["nome"],
                        "endereco": est["endereco"],
                        "lat": est["lat"],
                        "lon": est["lon"],
                        "categoria": est["categoria"]
                    })
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