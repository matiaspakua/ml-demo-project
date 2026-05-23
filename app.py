import tensorflow as tf
import numpy as np
import logging
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from flask import Flask, request, render_template
from flask.logging import create_logger

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

# This line creates an instance of the MobileNetV2 neural network model from Keras
# with pre-trained weights on the ImageNet dataset.
model = MobileNetV2(weights="imagenet")


@app.route("/")
def home():
    return render_template("view.html")

ALLOWED_EXTENSIONS = {".jpg"}


def allowed_file(filename):
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


# Preprocessing an image before feeding it into a neural network, specifically a MobileNetV2 model. It
# resizes the image to a square shape with dimensions of 224x224 pixels. MobileNetV2, expect input
# images of a specific size.
# The deep learning framework Keras preprocesses the image array to be compatible with the MobileNetV2
# model. It may involve normalization and other transformations.
def prepare_image(image):
    try:
        img = Image.open(image)
    except UnidentifiedImageError:
        LOG.error("Uploaded file is not a valid image")
        raise
    img = img.resize((224, 224))
    img_array = np.array(img)
    LOG.info("Format, resize and process image...")
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


# The model return a list of the top 3 posible results with highest probability.
@app.route("/predict", methods=["POST"])
def predict():
    image_file = request.files["image"]
    if image_file.filename == "" or not allowed_file(image_file.filename):
        LOG.warning(f"Invalid file type: {image_file.filename}")
        return render_template("view.html", error="Only .jpg images are allowed."), 400
    LOG.info("Processing image...")
    try:
        img_array = prepare_image(image_file)
    except UnidentifiedImageError:
        return render_template("view.html", error="The uploaded file is not a valid image."), 400
    LOG.info("Calling to model...")
    prediction = model.predict(img_array)
    results = tf.keras.applications.mobilenet_v2.decode_predictions(prediction, top=3)[0]
    response = []
    for result in results:
        response.append({"label": result[1], "probability": float(result[2])})
    return render_template("result.html", response=response)

# Expose the Flask application to port 8080.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
