from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)  # Wait time between tasks
    
   
    @task
    def access_home(self):
        self.client.get("/")
        
    @task
    def predict_image(self):
        # Simulate uploading an image file
        image_path = "images/test/image.jpg"
        with open(image_path, "rb") as image_file:
            files = {"image": image_file}
            self.client.post("/predict", files=files)