import logging
import tensorflow as tf

LOG = logging.getLogger(__name__)

MODEL_REGISTRY = {
    "mobilenet_v2": {
        "constructor": tf.keras.applications.MobileNetV2,
        "decode": tf.keras.applications.mobilenet_v2.decode_predictions,
        "label": "MobileNetV2",
        "params": "3.5M",
        "top1": "71.8%",
    },
    "mobilenet_v3": {
        "constructor": tf.keras.applications.MobileNetV3Large,
        "decode": tf.keras.applications.mobilenet_v3.decode_predictions,
        "label": "MobileNetV3 Large",
        "params": "5.4M",
        "top1": "75.8%",
    },
}


def get_model_info(model_name):
    info = MODEL_REGISTRY.get(model_name)
    if info is None:
        raise ValueError(f"Unknown model: {model_name}. Choices: {list(MODEL_REGISTRY.keys())}")
    return {
        "name": model_name,
        "label": info["label"],
        "params": info["params"],
        "top1": info["top1"],
    }


_loaded_models = {}


def load_model(model_name):
    if model_name in _loaded_models:
        return _loaded_models[model_name]

    info = MODEL_REGISTRY.get(model_name)
    if info is None:
        raise ValueError(f"Unknown model: {model_name}")

    LOG.info("Loading %s...", info["label"])
    model = info["constructor"](weights="imagenet")
    _loaded_models[model_name] = model
    return model


def decode_predictions(model_name, predictions, top=3):
    info = MODEL_REGISTRY.get(model_name)
    if info is None:
        raise ValueError(f"Unknown model: {model_name}")
    return info["decode"](predictions, top=top)
