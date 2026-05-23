import time
import logging
from werkzeug.exceptions import BadRequestKeyError
from flask import Flask, request, render_template
from flask.logging import create_logger

from src.image_utils import prepare_image, allowed_file
from src.model_loader import load_model, decode_predictions, get_model_info, MODEL_REGISTRY

app = Flask(__name__, template_folder="../templates")
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

DEFAULT_MODEL = "mobilenet_v2"


@app.context_processor
def inject_globals():
    model_info = {
        name: info["label"]
        for name, info in MODEL_REGISTRY.items()
    }
    return dict(models=model_info, default_model=DEFAULT_MODEL)


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
        LOG.warning("Invalid file type: %s", image_file.filename)
        return render_template("view.html", error="Only .jpg images are allowed."), 400

    model_name = request.form.get("model", DEFAULT_MODEL)
    if model_name not in MODEL_REGISTRY:
        model_name = DEFAULT_MODEL

    LOG.info("Processing image with %s...", model_name)
    t0 = time.time()

    try:
        img_array = prepare_image(image_file, model_name)
    except Exception:
        LOG.error("Uploaded file is not a valid image")
        return render_template("view.html", error="The uploaded file is not a valid image."), 400
    t1 = time.time()

    LOG.info("Calling model %s...", model_name)
    model = load_model(model_name)
    prediction = model.predict(img_array, verbose=0)
    t2 = time.time()

    results = decode_predictions(model_name, prediction, top=3)[0]
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

    model_info = get_model_info(model_name)
    return render_template("result.html", response=response, timing=timing, model=model_info)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8111, debug=True)
