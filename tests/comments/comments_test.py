import unittest
import requests
import jsonschema

from burrito.utils.config_reader import get_config

from tests.tickets.tickets_test import create_ticket_get_id
from tests.utils import get_access_token

from .schemas import *

TIMEOUT = 5


class CommentsTestCase(unittest.TestCase):
    def test_001_comments_create(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/comments/create",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "ticket_id": create_ticket_get_id("Make comment"),
                "body": "ya perdole kurva"
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        _response_schema = {
            "type": "object",
            "properties": {
                "detail": {"type": "string"},
                "comment_id": {"type": "string"}
            },
            "required": ["detail", "comment_id"]
        }

        jsonschema.validate(response.json(), _response_schema)

        return response.json()["comment_id"]

    def test_002_comments_edit(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/comments/edit",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "comment_id": self.test_001_comments_create(),
                "body": "ya perdole kurva (edited)"
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        _response_schema = {
            "type": "object",
            "properties": {
                "detail": {"type": "string"}
            },
            "required": ["detail"]
        }

        jsonschema.validate(response.json(), _response_schema)

    def test_003_comments_delete(self):
        response = requests.delete(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/comments/delete",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "comment_id": self.test_001_comments_create()
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        _response_schema = {
            "type": "object",
            "properties": {
                "detail": {"type": "string"}
            },
            "required": ["detail"]
        }

        jsonschema.validate(response.json(), _response_schema)

    def test_004_comments_create_multiple(self):
        ticket_id = create_ticket_get_id("Several comments")

        for _ in range(10):
            response = requests.post(
                f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/comments/create",
                headers={
                    "Authorization": f"Bearer {get_access_token()}"
                },
                json={
                    "ticket_id": ticket_id,
                    "body": "ya perdole kurva (several)"
                },
                timeout=TIMEOUT
            )

            assert response.status_code == 200

            _response_schema = {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "required": ["detail"]
            }

            jsonschema.validate(response.json(), _response_schema)

    def test_005_comments_get_comment(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/comments/get_comment_by_id",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "comment_id": self.test_001_comments_create()
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), test_005_comments_get_comment_schema)
