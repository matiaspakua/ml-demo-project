from pathlib import Path
import numpy as np
from PIL import Image, UnidentifiedImageError
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as mobilenet_v2_preprocess
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input as mobilenet_v3_preprocess


MODEL_INPUT_SIZE = (224, 224)
ALLOWED_EXTENSIONS = {".jpg"}


MODEL_PREPROCESSORS = {
    "mobilenet_v2": mobilenet_v2_preprocess,
    "mobilenet_v3": mobilenet_v3_preprocess,
}

MODEL_LABELS = {
    "mobilenet_v2": "MobileNetV2",
    "mobilenet_v3": "MobileNetV3",
}


def allowed_file(filename):
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def prepare_image(image, model_name="mobilenet_v2"):
    try:
        img = Image.open(image)
    except UnidentifiedImageError:
        raise
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize(MODEL_INPUT_SIZE)
    img_array = np.array(img)
    preprocess = MODEL_PREPROCESSORS.get(model_name, mobilenet_v2_preprocess)
    img_array = preprocess(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array
