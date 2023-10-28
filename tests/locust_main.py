from os import environ as ENV

from requests.exceptions import JSONDecodeError
from locust import HttpUser, SequentialTaskSet, task


class Meta:
    access_token = None


class TicketCreationTask(SequentialTaskSet):

    @task(1)
    def test_auth(self):
        response = self.client.post(
            "/auth/password/login",
            json={
                "login": ENV.get("LOCUST_LOGIN"),
                "password": ENV.get("LOCUST_PASSWORD")
            }
        )

        if not Meta.access_token:
            try:
                Meta.access_token = response.json()["access_token"]
            except JSONDecodeError:
                ...

    @task(2)
    def test_create_ticket(self):
        self.client.headers['Authorization'] = f"Bearer {Meta.access_token}"
        self.client.post(
            "/tickets/create",
            json={
                "subject": "dos attack",
                "body": "[dos attack] " * 9999,
                "hidden": False,
                "anonymous": True,
                "queue": 1,
                "faculty": 414,
            }
        )


class WebsiteUser(HttpUser):
    tasks = [TicketCreationTask]
    host = ENV.get("LOCUST_TARGET_HOST")
    max_wait = 9000
