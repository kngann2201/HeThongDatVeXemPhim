from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 3)
    @task(2)
    def get_courses(self):
        self.client.get("/")
    @task(1)
    def get_lessons(self):
        self.client.get("/bookings/13/")