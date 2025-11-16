"""this file is only temporary waiting for the API to be deployed"""

import numpy as np
from PIL import Image
import tensorflow as tf
from keras import Sequential, Model
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input as preprocess_input_vgg16
from keras.applications.densenet import preprocess_input as preprocess_input_densenet
from keras.applications.efficientnet_v2 import preprocess_input as preprocess_input_efficientnet

MODEL_DATA = {
    "densenet": {
        "label": "DenseNet",
        "preprocess_method": preprocess_input_densenet,
        "image_dim": (224, 224),
    },
    "vgg16": {
        "label": "VGG16",
        "preprocess_method": preprocess_input_vgg16,
        "image_dim": (256, 256),
    },
    "efficientnet": {
        "label": "EfficientNet",
        "preprocess_method": preprocess_input_efficientnet,
        "image_dim": (224, 224),
    },
}

def load_transfered_model(model_name: str) -> Sequential:
    model = load_model(
        f"models/{model_name}.keras",
        custom_objects={"preprocess_input": MODEL_DATA[model_name]["preprocess_method"]},
        safe_mode=False,
    )
    model.name = model_name

    return model

MODELS = [load_transfered_model(model_name) for model_name in MODEL_DATA.keys()]

def preprocess_image(img: Image.Image, model) -> np.ndarray:
    """Convert a PIL image into a tensor ready for DenseNet."""
    img = img.convert("RGB")
    img = img.resize(MODEL_DATA[model.name]["image_dim"])
    x = np.array(img, dtype=np.float32)
    x = MODEL_DATA[model.name]["preprocess_method"](x) # model builtin preprocessing
    x = np.expand_dims(x, axis=0) # batch of size 1

    return x

def predict_mole(image: Image.Image, model: Model):
    """Return (top_class_name, top_prob, full_dict_class_to_prob)."""
    x = preprocess_image(image, model)

    return model.predict(x)
