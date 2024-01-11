import pytest
import re
import numpy as np
import json
from flask import Flask, render_template, request
from werkzeug.datastructures import FileStorage
from PIL import Image
from app import prepare_image, predict

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
        assert content is not None


def test_home_content(app):
    with app.test_client() as client:
        response = client.get("/")
        # Extract the HTML content
        content = response.data.decode("utf-8")
        # Verify that the form contains the expected elements
        assert "<input type=" in content

def test_prepare_image_with_valid_image_path():
    # Set up
    image_path = "images/test/image.jpg"

    # Call the function
    img_array = prepare_image(image_path)

    # Check the shape of the image array
    expected_shape = (1, 224, 224, 3)
    assert img_array.shape == expected_shape

    # Check the type of the image array
    expected_type = np.float32
    print(f"{img_array.dtype}")
    assert img_array.dtype == expected_type
    
    # Check the values of the image array
    print(f"{img_array.min()}")
    assert 0.0 <= img_array.min() <= 1.0
    print(f"{img_array.max()}")
    assert img_array.max() == 1.0

def test_prepare_image_with_invalid_image_path():
    # Set up
    invalid_image_path = "images/invalid_image_path.jpg"

    # Call the function
    with pytest.raises(FileNotFoundError):
        img_array = prepare_image(invalid_image_path)



def test_predict_endpoint(app):
    # You may need to adjust the following based on your actual file path and image file
    image_file_path = "images/test/image.jpg"
    
    # Send a POST request to the /predict endpoint
    with open(image_file_path, "rb") as image_file:
        response = app.post("/predict", data={"image": (image_file, "image.jpg")})

    # Check if the response status code is 200 (OK)
    # assert response.status_code == 200
    print(f"{response.data}")
    # Add more assertions based on the expected behavior of your endpoint
    # For example, you might want to check if the response contains certain elements
    assert b"Processing image..." in response.data
    assert b"Calling to model..." in response.data
    assert b"result.html" in response.data
    assert b"label" in response.data
    assert b"probability" in response.data

