import pytest
from flask import Flask, render_template
import re


@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template("view.html")

    return app


def test_home_endpoint(app):
    with app.test_client() as client:
        response = client.get("/")

        assert response.status_code == 200
        assert response.mimetype == "text/html"
        content = response.data.decode("utf-8")
        # Check that the correct template is being used
        # assert "view.html" in response.data.decode('utf-8')
        assert content is not None


def test_home_content(app):
    with app.test_client() as client:
        response = client.get("/")

        # Extract the HTML content
        content = response.data.decode("utf-8")

        # print(f"content = {content}")

        # Verify that the form contains the expected elements
        assert "<input type=" in content
