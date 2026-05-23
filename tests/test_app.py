import pytest
import numpy as np
from io import BytesIO
from PIL import Image as PILImage
from app import prepare_image, allowed_file


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
        assert '<form id="uploadForm"' in content
        assert 'input type="file"' in content

    def test_home_contains_title(self, client):
        response = client.get("/")
        content = response.data.decode("utf-8")
        assert "ML Image Classification" in content


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


class TestAllowedFile:
    def test_allows_jpg(self):
        assert allowed_file("image.jpg") is True

    def test_allows_jpg_uppercase(self):
        assert allowed_file("image.JPG") is True

    def test_rejects_png(self):
        assert allowed_file("image.png") is False

    def test_rejects_no_extension(self):
        assert allowed_file("image") is False

    def test_rejects_empty_filename(self):
        assert allowed_file("") is False


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
        assert "Classification Results" in content

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

    def test_predict_rejects_png_file(self, client, valid_image_bytes):
        response = client.post(
            "/predict",
            data={"image": (valid_image_bytes, "test.png")},
            content_type="multipart/form-data",
        )
        assert response.status_code == 400
        content = response.data.decode("utf-8")
        assert "Only .jpg images are allowed" in content

    def test_predict_rejects_txt_file(self, client):
        response = client.post(
            "/predict",
            data={"image": (BytesIO(b"not an image"), "document.txt")},
            content_type="multipart/form-data",
        )
        assert response.status_code == 400
        content = response.data.decode("utf-8")
        assert "Only .jpg images are allowed" in content

    def test_predict_rejects_corrupted_jpg(self, client):
        response = client.post(
            "/predict",
            data={"image": (BytesIO(b"not an image"), "image.jpg")},
            content_type="multipart/form-data",
        )
        assert response.status_code == 400
        content = response.data.decode("utf-8")
        assert "not a valid image" in content

    def test_predict_rejects_empty_filename(self, client, valid_image_bytes):
        response = client.post(
            "/predict",
            data={"image": (valid_image_bytes, "")},
            content_type="multipart/form-data",
        )
        assert response.status_code == 400
