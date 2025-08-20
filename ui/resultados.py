import streamlit as st
import pandas as pd
import sqlite3
from utils.mapa import make_deck
import streamlit.components.v1 as components  # 👈 necessário para o widget de rota


# =======================================
# Widget de rota (minha localização / ponto no mapa)
# =======================================
def rota_widget(dest_lat: float, dest_lon: float, label_geo="Usar minha localização",
                label_mapa="Escolher no mapa", key: str = "rota", travelmode: str = "driving"):
    """
    Renderiza dois botões:
      - 'Usar minha localização': usa navigator.geolocation e abre a rota no Google Maps.
      - 'Escolher no mapa': abre um mini-mapa Leaflet; ao clicar no mapa, abre a rota a partir do ponto escolhido.

    travelmode: driving | walking | bicycling | transit
    """
    st.markdown(
        """
        <style>
        .rota-row { display:flex; gap:8px; flex-wrap:wrap; }
        .rota-btn {
            padding:8px 12px; border:none; border-radius:10px;
            background:#C077F3; color:#fff; font-weight:600; cursor:pointer;
        }
        .rota-btn:hover { background:#A355E2; }
        .map-wrap { margin-top:8px; }
        </style>
        """,
        unsafe_allow_html=True
    )

    html = f"""
<div class="rota-row">
  <button id="geo-{key}" class="rota-btn">🚗 {label_geo}</button>
  <button id="pick-{key}" class="rota-btn">🗺️ {label_mapa}</button>
</div>
<div id="map-wrap-{key}" class="map-wrap"></div>

<script>
(function(){{
  const destLat = {dest_lat};
  const destLon = {dest_lon};
  const mode = "{travelmode}";

  function openRoute(originLat, originLon){{
    const url = "https://www.google.com/maps/dir/?api=1"
      + "&origin=" + encodeURIComponent(originLat + "," + originLon)
      + "&destination=" + encodeURIComponent(destLat + "," + destLon)
      + "&travelmode=" + encodeURIComponent(mode);
    window.open(url, "_blank");
  }}

  function openFallback(){{
    const url = "https://www.google.com/maps/search/?api=1&query="
      + encodeURIComponent(destLat + "," + destLon);
    window.open(url, "_blank");
  }}

  // Minha localização (geolocalização do navegador)
  const geoBtn = document.getElementById("geo-{key}");
  geoBtn.addEventListener("click", function(){{
    if (!navigator.geolocation) {{
      openFallback();
      return;
    }}
    navigator.geolocation.getCurrentPosition(
      (pos)=>openRoute(pos.coords.latitude, pos.coords.longitude),
      ()=>openFallback(),
      {{ enableHighAccuracy:true, timeout:10000, maximumAge:60000 }}
    );
  }});

  // Escolher ponto no mapa (Leaflet + OSM)
  const pickBtn = document.getElementById("pick-{key}");
  pickBtn.addEventListener("click", function(){{
    const wrap = document.getElementById("map-wrap-{key}");
    if (wrap.dataset.inited) {{
      wrap.scrollIntoView({{behavior:'smooth', block:'center'}});
      return;
    }}
    wrap.dataset.inited = "1";
    const h = 260;
    wrap.innerHTML = '<div id="map-{key}" style="height:'+h+'px;border-radius:12px;overflow:hidden;"></div>';

    // CSS Leaflet
    const leafletCss = document.createElement('link');
    leafletCss.rel = 'stylesheet';
    leafletCss.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
    document.head.appendChild(leafletCss);

    // JS Leaflet
    const leafletJs = document.createElement('script');
    leafletJs.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
    leafletJs.onload = function(){{
      const map = L.map('map-{key}').setView([destLat, destLon], 14);
      L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap'
      }}).addTo(map);

      const destIcon = L.icon({{
        iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
        iconAnchor: [12, 41]
      }});
      L.marker([destLat, destLon], {{icon: destIcon}}).addTo(map)
        .bindPopup('Destino').openPopup();

      map.on('click', function(e){{
        const oLat = e.latlng.lat;
        const oLon = e.latlng.lng;
        openRoute(oLat, oLon);
      }});
    }};
    document.body.appendChild(leafletJs);
    wrap.scrollIntoView({{behavior:'smooth', block:'center'}});
  }});
}})();
</script>
"""
    components.html(html, height=320, scrolling=False)


# ================================
# Funções de acesso ao banco
# ================================
def _get_connection():
    return sqlite3.connect("data/estabelecimentos.db", check_same_thread=False)

def _filtrar_por_tipo(tipo_selecionado):
    conn = _get_connection()
    cursor = conn.cursor()
    if tipo_selecionado and tipo_selecionado != "Outros":
        cursor.execute(
            "SELECT nome, endereco, lat, lon, categoria FROM estabelecimentos WHERE categoria = ?",
            (tipo_selecionado,),
        )
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

    # (opcional) escolha do modo de deslocamento para o Google Maps
    cols_mode = st.columns([1, 3])
    with cols_mode[0]:
        modo = st.selectbox(
            "Modo",
            ["driving", "walking", "bicycling", "transit"],
            index=0,
            help="Modo de rota no Google Maps"
        )
    with cols_mode[1]:
        st.write("")

    tipo = st.session_state.get("tipo", "")
    filtrados = _filtrar_por_tipo(tipo)

    # Garante que o selecionado apareça
    selecionado = st.session_state.get("selecionado")
    filtrados = _garantir_selecionado_na_lista(filtrados, selecionado)

    st.markdown(f"##### Estabelecimentos encontrados ({tipo or 'Todos'}):")
    if not filtrados:
        st.info("Nenhum estabelecimento encontrado para o tipo selecionado.")
    else:
        for i, est in enumerate(filtrados):
            col1, col2, col3 = st.columns([4, 1, 2])
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
            with col3:
                # Botões: "Usar minha localização" e "Escolher no mapa" -> abre rota no Google Maps
                rota_widget(est['lat'], est['lon'], key=f"rota_{i}", travelmode=modo)

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
