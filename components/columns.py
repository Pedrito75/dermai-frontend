import streamlit as st
import altair as alt
import requests
import pandas as pd

from params import *
from callbacks import reset_image, scroll_to_bottom
from actions import try_predict

# ==================== LEFT ====================
def upload():
    st.markdown("## Upload a mole")

    mode = st.radio(
        "How do you want to provide a photo?",
        ("Upload a file", "Use camera"),
        horizontal=True,
        on_change=reset_image,
    )

    if mode == "Upload a file":

        if not st.session_state.is_uploaded:
            # Show uploader only if no image selected yet
            file = st.file_uploader(
                "Upload an image",
                type=["jpg", "jpeg", "png"],
                key="uploader"
            )
            if file:
                st.session_state.is_uploaded = True
                st.session_state.image = file
                st.rerun()

        else:
            st.image(st.session_state.image, caption="Uploaded image")
            if st.button("Choose another image"):
                st.session_state.is_uploaded = False
                st.rerun()
    else:
        st.session_state.is_uploaded = False
        picture = st.camera_input("Take a photo", on_change=reset_image)
        if picture:
            st.session_state.image = picture

# ==================== RIGHT ====================
def results(selected_model_label: str):
    with st.container(horizontal=True, vertical_alignment="bottom"):
        st.markdown("## Results")

        predict_btn = st.button("Predict", type="primary")#, on_click=scroll_to_bottom)

    with st.container(height="stretch", vertical_alignment="bottom"):
        if predict_btn:
            try_predict(selected_model_label)
