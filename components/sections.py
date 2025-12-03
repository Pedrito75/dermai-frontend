import streamlit as st

from params import *
from components.columns import upload, results

def model_selection():
    selected_model_label = st.selectbox(
        "Which asistant do you want for your prediction?",
        st.session_state.model_labels,
    )

    if not st.session_state.model_labels:
        st.error("Failed to fetch models from the API...")

    return selected_model_label

def metadata():
    st.markdown("## Add infos")
    col3, col4 = st.columns(2)
    with col3:
        zone_input = st.selectbox("Anatomical Zone", ZONES_LIST, key="zone_input")
    with col4:
        age_input = st.selectbox("Patient Age", AGES_LIST, key="age_input")

    return zone_input, age_input

def assistant(selected_model_label: str):
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            upload()

        with col2:
            results(selected_model_label)

def footer():
    st.markdown("""
        <hr>
        <div style="font-size: 0.8rem; color: gray; text-align: center;">
        <b>Disclaimer:</b> This tool is for informational and educational purposes only and does not provide a medical diagnosis.
        It should not be used as a substitute for professional medical advice, diagnosis, or treatment.
        Always consult a qualified healthcare provider regarding any concerns about skin lesions or moles.
        </div>
        """, unsafe_allow_html=True
    )
