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
    LOG.info(f"Accesing Root directory")
    return html.format(format)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
