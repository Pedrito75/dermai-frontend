import requests
import streamlit as st

from params import *
from components.sections import model_selection, metadata, assistant, footer

def page_setup():
    if "model_labels" not in st.session_state:
        try:
            model_names = requests.get(f"{SERVICE_URL}/models").json()
            model_names = [mn for mn in model_names if mn != "DenseNet"] # unhandled error with `DenseNet` model...
            st.session_state.model_labels = model_names
        except:
            st.session_state.model_labels = []

        st.session_state.is_uploaded = False
        st.session_state.image = None
        st.session_state.zone_input = "Head/Neck"
        st.session_state.age_input = "0-25 years old"

    st.set_page_config(page_title="DermAI", page_icon="🔍", layout="centered")

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

    footer()
