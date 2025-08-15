import streamlit as st

def tela_home():
    st.markdown("<h1 style='text-align: center;'>Encontre aqui</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: left;'>Encontre estabelecimentos do bairro desejado:</h3>", unsafe_allow_html=True)

    tipo = st.selectbox(
        "Escolha o tipo de estabelecimento:",
        ["", "Farmácias", "Mercados", "Lojas", "Hospitais", "Óticas", "Outros"],
        index=0,
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

    # Histórico (toggle)
    show_hist = st.toggle("Mostrar histórico (últimas 5 buscas)", value=False)
    if show_hist:
        ultimos = list(reversed(st.session_state.historico[-5:]))
        if not ultimos:
            st.write("Nenhuma busca recente.")
        else:
            for i, item in enumerate(ultimos):
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
                    st.link_button("Abrir no Google Maps", maps_url)