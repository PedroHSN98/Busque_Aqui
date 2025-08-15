import pandas as pd
import pydeck as pdk

def make_deck(estabelecimentos, selecionado=None):
    if not estabelecimentos:
        return None

    df = pd.DataFrame(estabelecimentos)
    layer_base = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[lon, lat]',
        get_fill_color='[0, 180, 0, 180]',
        get_radius=70,
        pickable=True,
    )
    layers = [layer_base]

    if selecionado:
        df_sel = pd.DataFrame([selecionado])
        layer_sel = pdk.Layer(
            "ScatterplotLayer",
            data=df_sel,
            get_position='[lon, lat]',
            get_fill_color='[255, 0, 0, 255]',
            get_radius=35,
            pickable=True,
        )
        layers.append(layer_sel)
        view_state = pdk.ViewState(
            latitude=float(selecionado["lat"]),
            longitude=float(selecionado["lon"]),
            zoom=16, pitch=0, bearing=0,
        )
    else:
        view_state = pdk.ViewState(
            latitude=float(df["lat"].mean()),
            longitude=float(df["lon"].mean()),
            zoom=12.5, pitch=0, bearing=0,
        )

    tooltip = {"text": "{nome}\n{endereco}"}
    return pdk.Deck(layers=layers, initial_view_state=view_state, map_style=None, tooltip=tooltip)