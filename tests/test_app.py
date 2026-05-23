import pytest
import numpy as np
from io import BytesIO
from PIL import Image as PILImage
from app import prepare_image


class TestHomeEndpoint:
    def test_home_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_home_returns_html(self, client):
        response = client.get("/")
        assert response.mimetype == "text/html"

    def test_home_contains_form(self, client):
        response = client.get("/")
        content = response.data.decode("utf-8")
        assert '<form action="/predict"' in content
        assert 'input type="file"' in content
        assert 'input type="submit"' in content

    def test_home_contains_title(self, client):
        response = client.get("/")
        content = response.data.decode("utf-8")
        assert "Python/Flask Image Classification App with ML" in content


class TestPrepareImage:
    def test_prepare_image_with_valid_path(self, valid_image_path):
        img_array = prepare_image(valid_image_path)

        assert img_array.shape == (1, 224, 224, 3)
        assert img_array.dtype == np.float32
        assert -2.0 <= img_array.min() <= 2.0
        assert img_array.max() <= 2.0

    def test_prepare_image_with_file_like_object(self):
        img = PILImage.new("RGB", (224, 224), color="blue")
        buf = BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)

        img_array = prepare_image(buf)

        assert img_array.shape == (1, 224, 224, 3)
        assert img_array.dtype == np.float32

    def test_prepare_image_raises_on_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            prepare_image("images/invalid_image_path.jpg")


class TestPredictEndpoint:
    def test_predict_returns_200_with_valid_image(self, client, valid_image_bytes):
        response = client.post(
            "/predict",
            data={"image": (valid_image_bytes, "test.jpg")},
            content_type="multipart/form-data",
        )
        assert response.status_code == 200

    def test_predict_returns_html(self, client, valid_image_bytes):
        response = client.post(
            "/predict",
            data={"image": (valid_image_bytes, "test.jpg")},
            content_type="multipart/form-data",
        )
        assert response.mimetype == "text/html"

    def test_predict_contains_results(self, client, valid_image_bytes):
        response = client.post(
            "/predict",
            data={"image": (valid_image_bytes, "test.jpg")},
            content_type="multipart/form-data",
        )
        content = response.data.decode("utf-8")
        assert "Image Classification Result" in content

    def test_predict_returns_400_without_image(self, client):
        response = client.post(
            "/predict",
            data={},
            content_type="multipart/form-data",
        )
        assert response.status_code == 400

    def test_predict_rejects_get_request(self, client):
        response = client.get("/predict")
        assert response.status_code == 405
