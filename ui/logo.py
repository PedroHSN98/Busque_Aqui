import base64
from pathlib import Path
import streamlit as st

LOGO_PATH = Path("assets/busque_aqui_logo.png")

def render_logo():
    if LOGO_PATH.exists():
        mime = "image/png" if LOGO_PATH.suffix.lower() == ".png" else "image/jpeg"
        data = LOGO_PATH.read_bytes()
        b64 = base64.b64encode(data).decode("utf-8")
        st.markdown(
            f'<img class="app-logo" src="data:{mime};base64,{b64}" alt="Busque Aqui logo" />',
            unsafe_allow_html=True,
        )