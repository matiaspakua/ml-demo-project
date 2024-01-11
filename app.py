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

# This line creates an instance of the MobileNetV2 neural network model from Keras 
# with pre-trained weights on the ImageNet dataset.
model = MobileNetV2(weights="imagenet")


@app.route("/")
def home():
    return render_template("view.html")

# Preprocessing an image before feeding it into a neural network, specifically a MobileNetV2 model. It 
# resizes the image to a square shape with dimensions of 224x224 pixels. MobileNetV2, expect input 
# images of a specific size.
# The deep learning framework Keras preprocesses the image array to be compatible with the MobileNetV2 
# model. It may involve normalization and other transformations.
def prepare_image(image):
    img = Image.open(image)
    img = img.resize((224, 224))
    img_array = np.array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


# The model return a list of the top 3 posible results with highest probability.
@app.route("/predict", methods=["POST"])
def predict():
    image = request.files["image"]
    LOG.info(f"Processing image...")
    img_array = prepare_image(image)
    LOG.info(f"Calling to model...")
    prediction = model.predict(img_array)
    results = tf.keras.applications.mobilenet_v2.decode_predictions(prediction, top=3)[0]
    response = []    
    for result in results:
        response.append({"label": result[1], "probability": float(result[2])})
    return render_template("result.html", response=response)    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
