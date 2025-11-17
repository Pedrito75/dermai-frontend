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
