import tensorflow as tf
import numpy as np
import logging
import mlib
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from flask import Flask, request, jsonify, render_template
from flask.logging import create_logger

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

model = MobileNetV2(weights="imagenet")


@app.route("/")
def home():
    return render_template("view.html")


def prepare_image(image):
    img = Image.open(image)
    img = img.resize((224, 224))
    img_array = np.array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


@app.route("/predict", methods=["POST"])
def predict():
    image = request.files["image"]
    LOG.info(f"Processing image...")
    img_array = prepare_image(image)
    LOG.info(f"Calling to model...")
    prediction = model.predict(img_array)
    results = tf.keras.applications.mobilenet_v2.decode_predictions(prediction, top=3)[
        0
    ]
    response = []
    for result in results:
        response.append({"label": result[1], "probability": float(result[2])})

    return render_template("result.html", response=response)
    # return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
