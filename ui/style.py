import streamlit as st

def inject_global_css():
    st.markdown(
        """
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
        """,
        unsafe_allow_html=True,
    )