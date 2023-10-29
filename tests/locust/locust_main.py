from multiprocessing import Queue
from os import environ as ENV

from locust import HttpUser, SequentialTaskSet, task


class BaseTask(SequentialTaskSet):
    class Meta:
        token = None
        access_tokens: Queue = Queue()
        refresh_tokens: Queue = Queue()

    def _prepare_auth_token(self):
        self.client.headers['Authorization'] = f"Bearer {self.Meta.token}"

    def on_start(self):
        response = self.client.post(
            "/auth/password/login",
            json={
                "login": ENV.get("LOCUST_LOGIN"),
                "password": ENV.get("LOCUST_PASSWORD")
            }
        )

        if not self.Meta.token:
            self.Meta.token = response.json()["access_token"]

        self.Meta.access_tokens.put(response.json()["access_token"])
        self.Meta.refresh_tokens.put(response.json()["refresh_token"])

    def on_stop(self):
        token = self.Meta.refresh_tokens.get()
        while token:
            # to delete token pair we need to send refresh token
            self.client.headers['Authorization'] = f"Bearer {token}"
            self.client.post("/auth/token/delete")

            token = self.Meta.refresh_tokens.get()

        token = self.Meta.access_tokens.get()
        while token:
            token = self.Meta.access_tokens.get()


class BurritoTask(BaseTask):
    @task
    def test_create_ticket(self):
        self._prepare_auth_token()
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
        return response

    @task
    def test_upload_file(self):
        self._prepare_auth_token()
        response = self.test_create_ticket()

        self.client.post(
            "/iofiles/upload_file",
            data={
                "ticket_id": response.json()["ticket_id"]
            },
            files=[('file_list', ('image.jpg', open("/image.jpg", "rb"), 'image/png')),]
        )

    @task
    def test_view_ticket_full_history(self):
        self._prepare_auth_token()
        response = self.test_create_ticket()

        self.client.post(
            "/tickets/full_history",
            json={
                "ticket_id": response.json()["ticket_id"]
            }
        )


class WebsiteUser(HttpUser):
    tasks = [BurritoTask]
    host = ENV.get("LOCUST_TARGET_HOST")
    max_wait = 9000
