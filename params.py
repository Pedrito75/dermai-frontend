import os
from dotenv import load_dotenv

load_dotenv(override=True)

# ----- api host -----
SERVICE_URL = os.getenv("SERVICE_URL")
# --------------------

# ----- dataset classes -----
CODE_TO_CLASS = {0: "akiec", 1: "bcc", 2: "bkl", 3: "df", 4: "mel", 5: "nv", 6: "vasc"}
CLASS_TO_NAME = {
    "akiec": "Actinic keratoses and intraepithelial carcinoma / Bowen's disease",
    "bcc": "Basal cell carcinoma",
    "bkl": "Benign keratosis-like lesions",
    "df": "Dermatofibroma",
    "mel": "Melanoma",
    "nv": "Melanocytic nevi",
    "vasc": "Vascular lesions",
}
COLOR_TO_HEXA = {
    "green": "#7EB42E",
    "yellow": "#EEFF34",
    "red": "#FF6F61",
}
CLASS_TO_COLOR = {
    "akiec": "yellow",
    "bcc": "red",
    "bkl": "green",
    "df": "green",
    "mel": "red",
    "nv": "green",
    "vasc": "green",
}
# ---------------------------

# ----- UI LISTS -----
ZONES_LIST = ["Head/Neck", "Trunk", "Upper Members", "Lower limbs", "Acral"]
AGES_LIST = ["0-25 years old", "26-50 years old", "51-70 years old", "> 70 years old"]
# ---------------------------

# ----- LOGIC MODIFIERS -----
# Combined dictionary: (Area, Age range) -> [Modifiers]
CONTEXT_MODIFIERS = {
    # --- HEAD/NECK ---
    ("Head/Neck", "0-25 years old"):  [-0.50, -0.80, -0.50, -0.20, -0.20, +0.50, -0.10],
    ("Head/Neck", "26-50 years old"): [-0.10, -0.20, +0.10, -0.10, +0.10, +0.10, +0.10],
    ("Head/Neck", "51-70 years old"): [+0.30, +0.30, +0.30, -0.20, +0.20, -0.30, +0.20],
    ("Head/Neck", "> 70 years old"):  [+0.50, +0.50, +0.40, -0.30, +0.30, -0.60, +0.30],

    # --- TRUNK (Back/Torso) ---
    ("Trunk", "0-25 years old"):      [-0.50, -0.50, -0.50, -0.10, -0.20, +0.40, -0.10],
    ("Trunk", "26-50 years old"):     [-0.20, -0.10, +0.10, +0.10, +0.20, +0.20, +0.20],
    ("Trunk", "51-70 years old"):     [-0.10, +0.10, +0.30, +0.10, +0.30, -0.20, +0.40],
    ("Trunk", "> 70 years old"):      [+0.10, +0.20, +0.50, -0.10, +0.30, -0.50, +0.50],

    # --- UPPER MEMBERS ---
    ("Upper Members", "0-25 years old"):  [-0.50, -0.50, -0.40, +0.10, -0.20, +0.40, -0.10],
    ("Upper Members", "26-50 years old"): [-0.10, -0.10, +0.10, +0.20, +0.10, +0.20, +0.10],
    ("Upper Members", "51-70 years old"): [+0.20, +0.10, +0.30, +0.10, +0.20, -0.20, +0.20],
    ("Upper Members", "> 70 years old"):  [+0.40, +0.20, +0.40, -0.10, +0.20, -0.50, +0.30],

    # --- LOWER LIMBS ---
    ("Lower limbs", "0-25 years old"):  [-0.50, -0.50, -0.40, +0.10, -0.20, +0.40, -0.10],
    ("Lower limbs", "26-50 years old"): [-0.20, -0.20, +0.10, +0.40, +0.20, +0.20, +0.10],
    ("Lower limbs", "51-70 years old"): [-0.10, +0.10, +0.30, +0.20, +0.30, -0.20, +0.20],
    ("Lower limbs", "> 70 years old"):  [+0.10, +0.20, +0.40, -0.10, +0.20, -0.50, +0.30],

    # --- ACRAL (Hands/Feet) ---
    ("Acral", "All Ages"): [-0.20, -0.50, -0.80, -0.20, +0.30, +0.20, -0.10]
}
# ---------------------------
