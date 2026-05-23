from pathlib import Path

from locust import HttpUser, between, task, tag


IMAGE_PATH = Path(__file__).resolve().parent.parent / "images" / "test" / "image.jpg"
WAIT_RANGE = (1, 5)
TOTAL_USERS = 10
SPAWN_RATE = 1


class HomepageUser(HttpUser):
    wait_time = between(*WAIT_RANGE)

    @task
    def access_home(self):
        with self.client.get("/", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Home returned {resp.status_code}")


class PredictV2User(HttpUser):
    wait_time = between(*WAIT_RANGE)

    @task
    def predict_with_v2(self):
        if not IMAGE_PATH.exists():
            self.client.get("/")
            return
        with open(IMAGE_PATH, "rb") as f:
            with self.client.post(
                "/predict",
                files={"image": f},
                data={"model": "mobilenet_v2"},
                catch_response=True,
            ) as resp:
                if resp.status_code != 200:
                    resp.failure(f"Predict V2 returned {resp.status_code}")
                elif "Classification Results" not in resp.text:
                    resp.failure("Predict V2 response missing results")

    @task
    def access_home(self):
        with self.client.get("/", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Home returned {resp.status_code}")


class PredictV3User(HttpUser):
    wait_time = between(*WAIT_RANGE)

    @task
    def predict_with_v3(self):
        if not IMAGE_PATH.exists():
            self.client.get("/")
            return
        with open(IMAGE_PATH, "rb") as f:
            with self.client.post(
                "/predict",
                files={"image": f},
                data={"model": "mobilenet_v3"},
                catch_response=True,
            ) as resp:
                if resp.status_code != 200:
                    resp.failure(f"Predict V3 returned {resp.status_code}")
                elif "Classification Results" not in resp.text:
                    resp.failure("Predict V3 response missing results")

    @task
    def access_home(self):
        with self.client.get("/", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Home returned {resp.status_code}")


class ErrorPathUser(HttpUser):
    wait_time = between(2, 8)

    @task
    def submit_without_image(self):
        with self.client.post("/predict", catch_response=True) as resp:
            if resp.status_code not in (400, 405):
                resp.failure(f"Expected 400/405, got {resp.status_code}")

    @task
    def submit_wrong_extension(self):
        with self.client.post(
            "/predict",
            files={"image": ("test.png", b"fake-image-data", "image/png")},
            catch_response=True,
        ) as resp:
            if resp.status_code != 400:
                resp.failure(f"Expected 400 for PNG, got {resp.status_code}")
