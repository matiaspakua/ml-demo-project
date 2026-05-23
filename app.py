import time
import tensorflow as tf
import numpy as np
import logging
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from werkzeug.exceptions import BadRequestKeyError
from flask import Flask, request, render_template
from flask.logging import create_logger

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

model = MobileNetV2(weights="imagenet")

MODEL_INPUT_SIZE = (224, 224)
ALLOWED_EXTENSIONS = {".jpg"}


def allowed_file(filename):
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def prepare_image(image):
    try:
        img = Image.open(image)
    except UnidentifiedImageError:
        LOG.error("Uploaded file is not a valid image")
        raise
    img = img.resize(MODEL_INPUT_SIZE)
    img_array = np.array(img)
    LOG.info("Format, resize and process image...")
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


@app.route("/")
def home():
    return render_template("view.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        image_file = request.files["image"]
    except BadRequestKeyError:
        return render_template("view.html", error="No image file provided."), 400
    if image_file.filename == "" or not allowed_file(image_file.filename):
        LOG.warning(f"Invalid file type: {image_file.filename}")
        return render_template("view.html", error="Only .jpg images are allowed."), 400

    LOG.info("Processing image...")
    t0 = time.time()

    try:
        img_array = prepare_image(image_file)
    except UnidentifiedImageError:
        return render_template("view.html", error="The uploaded file is not a valid image."), 400
    t1 = time.time()

    LOG.info("Calling to model...")
    prediction = model.predict(img_array)
    t2 = time.time()

    results = tf.keras.applications.mobilenet_v2.decode_predictions(prediction, top=3)[0]
    response = []
    for result in results:
        response.append({"label": result[1], "probability": float(result[2])})
    t3 = time.time()

    timing = {
        "preprocess_ms": round((t1 - t0) * 1000, 1),
        "inference_ms": round((t2 - t1) * 1000, 1),
        "decode_ms": round((t3 - t2) * 1000, 1),
        "total_ms": round((t3 - t0) * 1000, 1),
    }
    return render_template("result.html", response=response, timing=timing)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8111, debug=True)
