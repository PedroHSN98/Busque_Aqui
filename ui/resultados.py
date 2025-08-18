import streamlit as st
import pandas as pd
import sqlite3
from utils.mapa import make_deck


# ================================
# Funções de acesso ao banco
# ================================
def _get_connection():
    return sqlite3.connect("data/estabelecimentos.db", check_same_thread=False)

def _filtrar_por_tipo(tipo_selecionado):
    conn = _get_connection()
    cursor = conn.cursor()

    if tipo_selecionado and tipo_selecionado != "Outros":
        cursor.execute("SELECT nome, endereco, lat, lon, categoria FROM estabelecimentos WHERE categoria = ?", (tipo_selecionado,))
    else:
        cursor.execute("SELECT nome, endereco, lat, lon, categoria FROM estabelecimentos")

    rows = cursor.fetchall()
    conn.close()

    return [
        {"nome": r[0], "endereco": r[1], "lat": r[2], "lon": r[3], "categoria": r[4]}
        for r in rows
    ]


def _garantir_selecionado_na_lista(filtrados, selecionado):
    if not selecionado:
        return filtrados
    presente = any(
        (abs(e["lat"] - selecionado["lat"]) < 1e-9 and abs(e["lon"] - selecionado["lon"]) < 1e-9)
        or (e["nome"] == selecionado["nome"] and e["endereco"] == selecionado["endereco"]) 
        for e in filtrados
    )
    if not presente:
        return filtrados + [selecionado]
    return filtrados


def tela_resultados():
    st.markdown("<h2 style='text-align: center;'>Resultados da busca</h2>", unsafe_allow_html=True)

    tipo = st.session_state.get("tipo", "")
    filtrados = _filtrar_por_tipo(tipo)

    # Garante que o selecionado apareça
    selecionado = st.session_state.get("selecionado")
    filtrados = _garantir_selecionado_na_lista(filtrados, selecionado)

    st.markdown(f"##### Estabelecimentos encontrados ({tipo or 'Todos'}):")
    if not filtrados:
        st.info("Nenhum estabelecimento encontrado para o tipo selecionado.")
    else:
        for est in filtrados:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"*{est['nome']}* – {est['endereco']}")
            with col2:
                btn_key = f"visit_{est['nome']}_{est['endereco']}_{est['categoria']}"
                if st.button(f"Visitar {est['nome']}", key=btn_key):
                    st.session_state.historico.append({
                        "nome": est["nome"],
                        "endereco": est["endereco"],
                        "lat": est["lat"],
                        "lon": est["lon"],
                        "categoria": est["categoria"],
                    })
                    st.session_state.selecionado = est
                    st.rerun()

    st.markdown("### 📍 Mapa interativo da região")
    if filtrados:
        deck = make_deck(filtrados, selecionado=st.session_state.get("selecionado"))
        if deck:
            st.pydeck_chart(deck)
        else:
            st.write("Sem dados para exibir no mapa.")
    else:
        st.write("Sem dados para exibir no mapa.")

    if st.button("Voltar"):
        st.session_state.pagina = "home"
        st.session_state.selecionado = None