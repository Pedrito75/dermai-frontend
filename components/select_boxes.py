import streamlit as st

def select_model():
    selected_model_label = st.selectbox(
        "Which asistant do you want for your prediction?",
        st.session_state.model_labels,
    )

    if not st.session_state.model_labels:
        st.error("Failed to fetch models from the API...")

    return selected_model_label
