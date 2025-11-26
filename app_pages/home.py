import requests
import pandas as pd
from PIL import Image
import streamlit as st
import altair as alt

from params import *
from components.select_boxes import select_model
from components.containers import assistant

def page_setup():
    if "model_labels" not in st.session_state:
        try:
            st.session_state.model_labels = requests.get(f"{SERVICE_URL}/models").json()
        except:
            st.session_state.model_labels = []

    if "is_uploaded" not in st.session_state:
        st.session_state.is_uploaded = False

    if "image" not in st.session_state:
        st.session_state.image = None

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

    selected_model_label = select_model()

    assistant(selected_model_label)
