import requests
import streamlit as st

from params import *
from components.containers import model_selection, metadata, assistant

def page_setup():
    if "model_labels" not in st.session_state:
        try:
            st.session_state.model_labels = requests.get(f"{SERVICE_URL}/models").json()
        except:
            st.session_state.model_labels = []

        st.session_state.is_uploaded = False
        st.session_state.image = None
        st.session_state.zone_input = "Head/Neck"
        st.session_state.age_input = "0-25 years old"

    # if "is_uploaded" not in st.session_state:
        # st.session_state.is_uploaded = False

    # if "image" not in st.session_state:
        # st.session_state.image = None

    # if "zone_input" not in st.session_state:
    #     st.session_state.zone_input = "Head/Neck"

    # window tile setup
    st.set_page_config(page_title="DermAI", page_icon="🔍", layout="centered")

    # add css styling
    with open('./styles.css') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    st.header("DermAI Assistant", divider="grey")

    st.markdown("## Choose your model")

def home_page():
    page_setup()

    selected_model_label = model_selection()

    metadata()

    assistant(selected_model_label)
