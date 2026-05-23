import pytest
from io import BytesIO
from PIL import Image as PILImage


VALID_IMAGE_PATH = "images/test/image.jpg"


@pytest.fixture
def app():
    from app import app as flask_app
    flask_app.config.update({"TESTING": True})
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def valid_image_path():
    return VALID_IMAGE_PATH


@pytest.fixture
def valid_image_bytes():
    img = PILImage.new("RGB", (224, 224), color="red")
    buf = BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf


@pytest.fixture(autouse=True)
def mock_model(monkeypatch):
    import numpy as np
    class MockModel:
        def predict(self, img_array):
            predictions = np.zeros((1, 1000))
            predictions[0, 1] = 0.8
            predictions[0, 2] = 0.15
            predictions[0, 3] = 0.05
            return predictions
    monkeypatch.setattr("app.model", MockModel())
