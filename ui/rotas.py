# ui/rotas.py
import streamlit as st
import streamlit.components.v1 as components

def rota_widget(dest_lat: float, dest_lon: float, label_geo="Usar minha localização", label_mapa="Escolher no mapa", key: str = "rota", travelmode: str = "driving"):
    """
    Renderiza dois botões:
    - 'Usar minha localização': usa navigator.geolocation e abre a rota no Google Maps.
    - 'Escolher no mapa': abre um mini-mapa (Leaflet). Ao clicar, abre a rota a partir do ponto escolhido.

    travelmode pode ser: driving | walking | bicycling | transit
    """
    # estilos básicos
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

    # HTML+JS do componente
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

  // Botão: Minha localização
  document.getElementById("geo-{key}").addEventListener("click", function(){{
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

  // Botão: Escolher no mapa (Leaflet + OSM)
  const pickBtn = document.getElementById("pick-{key}");
  pickBtn.addEventListener("click", function(){{
    const wrap = document.getElementById("map-wrap-{key}");
    if (wrap.dataset.inited) {{
      // se já existe, apenas rola até o mapa
      wrap.scrollIntoView({{behavior:'smooth', block:'center'}});
      return;
    }}
    wrap.dataset.inited = "1";
    const h = 260;  // altura do mapa
    wrap.innerHTML = '<div id="map-{key}" style="height:'+h+'px;border-radius:12px;overflow:hidden;"></div>';

    // injeta Leaflet (CSS + JS) via CDN
    const leafletCss = document.createElement('link');
    leafletCss.rel = 'stylesheet';
    leafletCss.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
    document.head.appendChild(leafletCss);

    const leafletJs = document.createElement('script');
    leafletJs.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
    leafletJs.onload = function(){{
      // inicializa mapa centralizado no destino
      const map = L.map('map-{key}').setView([destLat, destLon], 14);
      L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap'
      }}).addTo(map);

      // marcador do destino
      const destIcon = L.icon({{
        iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
        iconAnchor: [12, 41]
      }});
      L.marker([destLat, destLon], {{icon: destIcon}}).addTo(map)
        .bindPopup('Destino').openPopup();

      // clique no mapa => abre rota
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
