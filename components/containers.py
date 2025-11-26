import streamlit as st

from params import *
from components.columns import upload, results

def assistant(selected_model_label: str):
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            upload()

        with col2:
            results(selected_model_label)
