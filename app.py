from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging

import mlib

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)


@app.route("/")
def home():
    html = f"<h3>Hello World Python Flask</h3>"
    return html.format(format)
