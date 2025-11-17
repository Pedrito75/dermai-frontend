import requests
import pandas as pd
from PIL import Image
import streamlit as st

from params import *

if "model_labels" not in st.session_state:
    st.session_state.model_labels = requests.get(f"{SERVICE_URL}/models").json()

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

selected_model_label = st.selectbox(
    "Which asistant do you want for your prediction?",
    st.session_state.model_labels,
)

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## Upload a mole")

        mode = st.radio(
            "How do you want to provide a photo?",
            ("Upload a file", "Use camera"),
            horizontal=True,
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
            picture = st.camera_input("Take a photo")
            if picture:
                st.session_state.image = picture

    with col2:
        with st.container(horizontal=True, vertical_alignment="bottom"):
            st.markdown("## Results")

            predict_btn = st.button("Predict", type="primary")

        with st.container(height="stretch", vertical_alignment="bottom"):
            if predict_btn:
                if not st.session_state.image:
                    st.warning("You need add an image!")
                else:
                    with st.spinner(text="Predicting your fate...", show_time=True):
                        # image = Image.open(st.session_state.image)
                        image = st.session_state.image
                        files = {
                            "img": (image.name, image.getbuffer(), image.type)
                        }

                        data = {
                            "model_label": selected_model_label
                        }
                        response = requests.post(f"{SERVICE_URL}/predict", data=data, files=files)

                        pred = pd.DataFrame(response.json()).set_index("index")

                        with st.container(height="stretch", vertical_alignment="top"):
                            best_pred = pred.iloc[0]
                            class_pred = CLASS_TO_NAME[best_pred.name]
                            if best_pred["color"] == "green":
                                st.success(f"You should be fine 👌\nI bet it's a `{class_pred}`")
                            elif best_pred["color"] == "yellow":
                                st.warning(f"Hum this is weird 🤔\nI recommend you check what could be a `{class_pred}` when you have time")
                            else:
                                st.error(f"It looks like a `{class_pred}` ⚠️\nDon't wait to see a professional")

                        st.bar_chart(data=pred, y="Probabilities", color="hexa", horizontal=True, sort="-Probabilities")
