import requests
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

from params import *

# ==============================================================================
# HELPER FUNCTIONS (Logic moved from testing to app for display purposes)
# ==============================================================================
def adjust_predictions(initial_probs: list, anatom_zone: str, age_range: str):
    """Ajuste les probas selon le tableau Excel (Logique locale)"""
    # Gestion du cas spécial Acral qui ignore l'âge
    search_key = ("Acral", "All Ages") if anatom_zone == "Acral" else (anatom_zone, age_range)
    modifiers = CONTEXT_MODIFIERS.get(search_key)

    if modifiers is None:
        modifiers = [0.0] * 7

    modifiers = np.array(modifiers)
    base_probs = np.array(initial_probs)

    # Calcul : Proba initiale + Modificateur
    new_probs = base_probs + modifiers
    # Clip pour rester entre 0 et 1
    new_probs = np.clip(new_probs, 0.0, 1.0)
    # Renormalisation pour que la somme fasse 100%
    if np.sum(new_probs) > 0:
        new_probs = new_probs / np.sum(new_probs)

    return new_probs.tolist()

# ==============================================================================
# SESSION STATE SETUP
# ==============================================================================
if "model_labels" not in st.session_state:
    # Fallback if API is down just for UI loading
    st.session_state.model_labels = ["DermAI Model v1"]
    try:
        st.session_state.model_labels = requests.get(f"{SERVICE_URL}/models").json()
    except:
        pass

if "is_uploaded" not in st.session_state:
    st.session_state.is_uploaded = False

if "image" not in st.session_state:
    st.session_state.image = None

# NEW: Track mole validation status
if "mole_check_done" not in st.session_state:
    st.session_state.mole_check_done = False
if "is_valid_mole" not in st.session_state:
    st.session_state.is_valid_mole = False

# ==============================================================================
# PAGE CONFIG & STYLING
# ==============================================================================
st.set_page_config(page_title="DermAI", page_icon="🔍", layout="centered")

with open('./styles.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.header("DermAI Assistant", divider="grey")

# ==============================================================================
# MAIN INTERFACE
# ==============================================================================

# 1. MODEL SELECTION
st.markdown("## Choose your model")
selected_model_label = st.selectbox(
    "Which asistant do you want for your prediction?",
    st.session_state.model_labels,
)

with st.container(border=True):
    # --- SECTION UPLOAD ---
    st.markdown("## 1. Upload a mole")

    mode = st.radio(
        "How do you want to provide a photo?",
        ("Upload a file", "Use camera"),
        horizontal=True,
    )

    # Logic to handle Image Upload / Camera
    new_image = None
    if mode == "Upload a file":
        if not st.session_state.is_uploaded:
            file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], key="uploader")
            if file:
                new_image = file
        else:
            st.image(st.session_state.image, caption="Uploaded image", width=200)
            if st.button("Choose another image"):
                # Reset ALL states
                st.session_state.is_uploaded = False
                st.session_state.image = None
                st.session_state.mole_check_done = False
                st.session_state.is_valid_mole = False
                st.rerun()
    else:
        # Camera mode
        picture = st.camera_input("Take a photo")
        if picture:
            new_image = picture
            st.session_state.is_uploaded = True # Force upload state for cam

    # Handle new image arrival
    if new_image is not None and not st.session_state.mole_check_done:
        st.session_state.image = new_image
        st.session_state.is_uploaded = True

        # --- AUTOMATIC STEP: CHECK IS MOLE ---
        with st.spinner("Checking if this is a valid mole..."):
            image_file = st.session_state.image
            files = {"img": (image_file.name, image_file.getbuffer(), image_file.type)}

            try:
                # ⚠️ CALL TO API: /check-mole
                # Assumes API returns JSON: {"is_mole": boolean}
                res = requests.post(f"{SERVICE_URL}/check-mole", files=files)

                if res.status_code == 200:
                    is_mole = res.json().get("is_mole", False)
                    st.session_state.mole_check_done = True
                    st.session_state.is_valid_mole = is_mole
                    st.rerun()
                else:
                    st.error("Error communicating with verification server.")
            except Exception as e:
                # FOR DEMO IF API IS NOT READY, UNCOMMENT BELOW TO BYPASS
                # st.session_state.mole_check_done = True
                # st.session_state.is_valid_mole = True
                # st.rerun()
                st.error(f"Connection error: {e}")

    # ==========================================================================
    # LOGIC FLOW AFTER UPLOAD
    # ==========================================================================

    # CASE A: NOT A MOLE
    if st.session_state.mole_check_done and not st.session_state.is_valid_mole:
        st.error("⚠️ No mole detected / Pas de grain de beauté détecté.")
        st.warning("Please upload a clear picture of a mole / Veuillez uploader une photo claire d'un grain de beauté.")
        if st.button("Try again"):
            st.session_state.is_uploaded = False
            st.session_state.mole_check_done = False
            st.session_state.image = None
            st.rerun()

    # CASE B: VALID MOLE -> SHOW CONTEXT FIELDS & PREDICT
    if st.session_state.mole_check_done and st.session_state.is_valid_mole:
        st.success("✅ Valid mole detected.")

        st.markdown("## 2. Clinical Context")

        c1, c2 = st.columns(2)
        with c1:
            zone_input = st.selectbox("Anatomical Zone", ZONES_LIST)
        with c2:
            age_input = st.selectbox("Patient Age", AGES_LIST)

        st.markdown("## 3. Analysis")
        predict_btn = st.button("Run Full Analysis", type="primary")

        if predict_btn:
             with st.spinner(text="Analyzing lesion and adjusting probabilities..."):
                image = st.session_state.image
                files = {
                    "img": (image.name, image.getbuffer(), image.type)
                }
                data = {
                    "model_label": selected_model_label
                }

                # 1. GET RAW PREDICTIONS FROM API
                try:
                    response = requests.post(f"{SERVICE_URL}/predict", data=data, files=files)

                    if response.status_code == 200:
                        # Assuming API returns a dict/list of probabilities in correct order
                        # Example response format expected from API: {"probabilities": [0.1, 0.2, ...]}
                        # OR the previous format dict where values are probabilities.
                        # We need the RAW list of floats matching CLASSES_7 order.

                        resp_json = response.json()

                        # --- ADAPTING TO YOUR API FORMAT ---
                        # Si l'API renvoie déjà un format dataframe-ready, on extrait les probas brutes
                        # On suppose ici que l'API renvoie quelque chose que l'on peut mapper.
                        # Pour simplifier l'intégration du test : on attend une liste ou un dict.

                        # Fallback extraction logic (Modify based on actual API response structure)
                        if isinstance(resp_json, list):
                             raw_probs = resp_json # If API returns just list of floats
                        elif "probabilities" in resp_json:
                             raw_probs = resp_json["probabilities"]
                        else:
                             # If API returns detailed dict, extract values in order of CLASSES_7
                             # This is fragile, better if API sends list.
                             # Let's assume standard values extraction if keys match CLASSES_7
                             raw_probs = [resp_json.get(k, 0.0) for k in CLASSES_7]

                        # 2. APPLY LOCAL ADJUSTMENT (The logic you wanted)
                        adj_probs = adjust_predictions(raw_probs, zone_input, age_input)

                        # 3. BUILD DATAFRAME FOR DISPLAY
                        df_results = pd.DataFrame({
                            "Lesion Type": [CLASS_TO_NAME[c] for c in CLASSES_7],
                            "Raw Prob (AI)": raw_probs,
                            "Adjusted Prob (Context)": adj_probs
                        })

                        # Find best prediction
                        best_idx = np.argmax(adj_probs)
                        best_class_code = CLASSES_7[best_idx]
                        best_class_name = CLASS_TO_NAME[best_class_code]
                        best_color = CLASS_TO_COLOR[best_class_code]

                        # 4. DISPLAY RESULT CARDS
                        with st.container():
                            if best_color == "green":
                                st.success(f"Diagnosis: **{best_class_name}** (Low Risk) 👌")
                            elif best_color == "yellow":
                                st.warning(f"Diagnosis: **{best_class_name}** (Monitor) 🤔")
                            else:
                                st.error(f"Diagnosis: **{best_class_name}** (Consult Doctor) ⚠️")

                        # 5. DISPLAY THE REQUESTED DOUBLE TABLE
                        st.subheader("Detailed Probability Analysis")

                        # Formatting for display
                        df_display = df_results.copy()
                        df_display["Raw Prob (AI)"] = df_display["Raw Prob (AI)"].apply(lambda x: f"{x:.1%}")
                        df_display["Adjusted Prob (Context)"] = df_display["Adjusted Prob (Context)"].apply(lambda x: f"{x:.1%}")
                        df_display["Delta"] = (np.array(adj_probs) - np.array(raw_probs))
                        df_display["Delta"] = df_display["Delta"].apply(lambda x: f"{x:+.1%}")

                        st.table(df_display)

                        # Optional: Keep the chart
                        st.bar_chart(df_results.set_index("Lesion Type")["Adjusted Prob (Context)"])

                    else:
                        st.error(f"API Error: {response.status_code}")

                except Exception as e:
                    st.error(f"Analysis failed: {e}")
