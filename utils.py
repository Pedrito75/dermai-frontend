import numpy as np
import pandas as pd

from params import CONTEXT_MODIFIERS

def adjust_predictions(raw_pred: pd.DataFrame, anatom_zone: str, age_range: str) -> pd.DataFrame:
    """
    Adjust softmax probabilities using contextual modifiers.
    Modifiers are applied in logit space → correct Bayesian-style update.
    """

    adjusted_pred = raw_pred.copy()

    # Special case: Acral
    key = ("Acral", "All Ages") if anatom_zone == "Acral" else (anatom_zone, age_range)
    modifiers = CONTEXT_MODIFIERS.get(key, [0.0] * 7)
    modifiers = np.array(modifiers)

    # Extract original probabilities (vector of length 7)
    base_probs = np.array(adjusted_pred["Probabilities"])

    # Safety: normalize if not already
    base_probs = base_probs / np.sum(base_probs)

    # Convert probabilities -> logits
    eps = 1e-12
    logits = np.log(base_probs + eps)

    # Apply contextual modifiers in logit space
    new_logits = logits + modifiers

    # Softmax to return to probability space
    exp_vals = np.exp(new_logits - np.max(new_logits))  # stability
    new_probs = exp_vals / np.sum(exp_vals)

    adjusted_pred["Probabilities"] = new_probs.tolist()
    return adjusted_pred
