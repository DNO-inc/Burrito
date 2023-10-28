from os import environ as ENV
from sys import stderr as STDERR

from requests.exceptions import JSONDecodeError
from locust import HttpUser, SequentialTaskSet, task


class BaseTask(SequentialTaskSet):
    class Meta:
        access_token = None

    @task(1)
    def test_auth(self):
        response = self.client.post(
            "/auth/password/login",
            json={
                "login": ENV.get("LOCUST_LOGIN"),
                "password": ENV.get("LOCUST_PASSWORD")
            }
        )

        if not self.Meta.access_token:
            try:
                self.Meta.access_token = response.json()["access_token"]
            except JSONDecodeError:
                ...


class BurritoTask(BaseTask):
    @task(2)
    def test_create_ticket(self):
        self.client.headers['Authorization'] = f"Bearer {self.Meta.access_token}"
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

    @task(3)
    def test_upload_file(self):
        self.client.headers['Authorization'] = f"Bearer {self.Meta.access_token}"
        response = self.client.post(
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

        try:
            self.client.post(
                "/iofiles/upload_file",
                data={
                    "ticket_id": response.json()["ticket_id"]
                },
                files=[('file_list', ('image.jpg', open("/image.jpg", "rb"), 'image/png')),]
            )
        except Exception as e:
            print(e, file=STDERR)


class WebsiteUser(HttpUser):
    tasks = [BurritoTask]
    host = ENV.get("LOCUST_TARGET_HOST")
    max_wait = 9000
