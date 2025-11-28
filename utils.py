import numpy as np
import pandas as pd

from params import CONTEXT_MODIFIERS

def adjust_predictions(raw_pred: pd.DataFrame, anatom_zone: str, age_range: str) -> pd.DataFrame:
    """Ajuste les probas selon le tableau Excel (Logique locale)"""
    # Gestion du cas spécial Acral qui ignore l'âge
    adjusted_pred = raw_pred.copy()
    search_key = ("Acral", "All Ages") if anatom_zone == "Acral" else (anatom_zone, age_range)
    modifiers = CONTEXT_MODIFIERS.get(search_key)

    if modifiers is None:
        modifiers = [0.0] * 7

    modifiers = np.array(modifiers)
    base_probs = np.array(adjusted_pred["Probabilities"])

    # Calcul : Proba initiale + Modificateur
    new_probs = base_probs + modifiers
    # Clip pour rester entre 0 et 1
    new_probs = np.clip(new_probs, 0.0, 1.0)
    # Renormalisation pour que la somme fasse 100%
    if np.sum(new_probs) > 0:
        new_probs = new_probs / np.sum(new_probs)

    adjusted_pred["Probabilities"] = new_probs.tolist()
    return adjusted_pred
