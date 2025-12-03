import streamlit as st
import altair as alt
import requests
import pandas as pd
# from pprint import pprint

from params import *
from components.charts import results_chart
from utils import adjust_predictions

# from callbacks import scroll_to_bottom

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
    # print(response)
    # print(response.status_code)

    zone_input, age_input = st.session_state.zone_input, st.session_state.age_input

    # print("\n==================== Raw pred ====================\n")
    raw_pred = pd.DataFrame(response.json())
    # pprint(raw_pred)

    adjusted_pred = adjust_predictions(raw_pred, zone_input, age_input)

    # print("\n==================== Adjusted pred ====================\n")
    # print(zone_input, age_input)
    # pprint(adjusted_pred)

    adjusted_pred.sort_values(by="Probabilities", ascending=False, inplace=True)
    # print("\n==================== Sorted adjusted pred ====================\n")
    # pprint(adjusted_pred)

    adjusted_pred.reset_index(drop=True, inplace=True)

    with st.container(height="stretch", vertical_alignment="top", key="results_div"):
        # best_pred = raw_pred.iloc[0]
        best_pred = adjusted_pred.iloc[0]
        class_pred = CLASS_TO_NAME[best_pred["index"]]
        if best_pred["color"] == "green":
            st.success(f"You should be fine 👌\nI bet it's a `{class_pred}`")
        elif best_pred["color"] == "yellow":
            st.warning(f"Hum this is weird 🤔\nI recommend you check what could be a `{class_pred}` when you have time")
        else:
            st.error(f"It looks like a `{class_pred}` ⚠️\nDon't wait to see a professional")

    # results_chart(raw_pred)
    results_chart(adjusted_pred)

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
