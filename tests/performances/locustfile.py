from locust import HttpUser, TaskSet, between, task

class PerfTest(TaskSet):
    wait_time = between(1, 2)

    @task
    def index(self):
        self.client.get("/")

    @task
    def show_summary(self):
        self.client.post("/show-summary", data={"email": "john@simplylift.co"})

    @task
    def purchase_places(self):
        self.client.post(
            "/purchase-places",
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": 1,
            },
        )

    @task
    def logout(self):
        self.client.get("/logout")

class WebsiteUser(HttpUser):
    tasks = [PerfTest]
    wait_time = between(1, 2)