import time
import uuid
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    

    def on_start(self):
        # Assign a unique identifier to each instance
        self.user_id = str(uuid.uuid4())

    @task
    def view_imgs(self):
        # Use the unique identifier in your task
        print(f"User {self.user_id} is viewing images")
        self.client.get("/uploads")

    @task(4)
    def load_img(self):
        custom_file_name = f"{self.user_id}_image.png"  # Custom file name to be used on the server
        with open("image.png", "rb") as img:
            self.client.post("/", files={"file": (custom_file_name, img)})
        print(f"User {self.user_id} uploaded an image as {custom_file_name}")
