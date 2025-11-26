import streamlit as st
import altair as alt
import requests
import pandas as pd

from params import *
from callbacks import scroll_to_bottom

def check_relevance(files: dict) -> bool:
    security_response = requests.post(f"{SERVICE_URL}/control", files=files)
    if not security_response.status_code == 200:
        st.error("Something broke in the backend side")
        return False

    if security_response.json()["security"] == "passed":
        return True

    return False

def show_results(data: dict, files: dict):
    response = requests.post(f"{SERVICE_URL}/predict", data=data, files=files)

    pred = pd.DataFrame(response.json())

    with st.container(height="stretch", vertical_alignment="top"):
        best_pred = pred.iloc[0]
        class_pred = CLASS_TO_NAME[best_pred["index"]]
        if best_pred["color"] == "green":
            st.success(f"You should be fine 👌\nI bet it's a `{class_pred}`")
        elif best_pred["color"] == "yellow":
            st.warning(f"Hum this is weird 🤔\nI recommend you check what could be a `{class_pred}` when you have time")
        else:
            st.error(f"It looks like a `{class_pred}` ⚠️\nDon't wait to see a professional")

    chart = (
        alt.Chart(pred)
        .mark_bar()
        .encode(
            y=alt.Y("index:N", sort="-x"),
            x=alt.X("Probabilities:Q"),
            color=alt.Color("hexa:N", scale=None),
            tooltip=["Probabilities"],
        )
    )
    st.altair_chart(chart, width="stretch")

def try_predict(selected_model_label: str):
    if not st.session_state.image:
        st.warning("You need add an image!")
    else:
        with st.spinner(text="Predicting your fate...", show_time=True):
            image = st.session_state.image

            files = {
                "img": (image.name, image.getbuffer(), image.type)
            }

            data = {
                "model_label": selected_model_label
            }

            is_relevant = check_relevance(files)

            if is_relevant:
                show_results(data, files)
            else:
                st.warning("You little joker, that's not a mole 😅")

    # scroll_to_bottom()
