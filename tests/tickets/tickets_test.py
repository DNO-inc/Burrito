import unittest
import string
import random

import requests
import jsonschema

from burrito.utils.config_reader import get_config

from tests.utils import get_access_token

from .schemas import *


TIMEOUT = 10


def create_ticket_get_id(subject: str) -> int:
    response = requests.post(
        f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/create",
        headers={
            "Authorization": f"Bearer {get_access_token()}"
        },
        json={
            "subject": subject,
            "body": "".join([random.choice(string.ascii_letters) for i in range(700)]),
            "hidden": True if random.randint(0, 9) % 2 == 0 else False,
            "anonymous": True if random.randint(0, 9) % 2 == 0 else False,
            "queue": 1,
            "faculty": 414,
        },
        timeout=TIMEOUT
    )

    assert response.status_code == 200

    _response_schema = {
        "type": "object",
        "properties": {
            "detail": {"type": "string"},
            "ticket_id": {"type": "number"}
        },
        "required": ["detail", "ticket_id"]
    }

    jsonschema.validate(response.json(), _response_schema)

    return response.json()["ticket_id"]


class TicketsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.first_ticket = 0

    def test_001_create_ticket(self):
        """Create ticket"""

        TicketsTestCase.first_ticket = create_ticket_get_id("".join(random.sample(string.ascii_letters, 10)))

    def test_002_delete_ticket(self):
        """Delete ticket"""

        ticket_id = create_ticket_get_id("for black list")

        response = requests.delete(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/delete",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "ticket_id_list": [ticket_id]
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), detail_response_schema_template)


    def test_003_delete_ticket_noexist(self):
        """Delete ticket"""

        response = requests.delete(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/delete",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "ticket_id_list": [TicketsTestCase.first_ticket + 123456]
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 403

        jsonschema.validate(response.json(), detail_response_schema_template)

    def test_004_like_ticket(self):
        """Delete ticket"""

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/like",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "ticket_id": create_ticket_get_id("to like")
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), detail_response_schema_template)

    def test_005_like_ticket_noexist(self):
        """Delete ticket"""

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/like",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "ticket_id": TicketsTestCase.first_ticket + 123456
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 403

        jsonschema.validate(response.json(), detail_response_schema_template)

    def test_006_bookmark_ticket(self):
        """Bookmark ticket"""

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/bookmark",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "ticket_id": create_ticket_get_id("to bookmark")
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), detail_response_schema_template)

    def test_007_bookmark_ticket_noexist(self):
        """Bookmark ticket"""

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/bookmark",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "ticket_id": TicketsTestCase.first_ticket + 123456
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 403

        jsonschema.validate(response.json(), detail_response_schema_template)

    def test_008_tickets_filter(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/ticket_list",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "anonymous": True,
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), tickets_list_response_schema_template)

    def test_009_ticket_detail_view(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/show",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "ticket_id": create_ticket_get_id("show info about ticket")
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), test_009_ticket_detail_view_schemas)

    def test_010_update_ticket(self):
        """Update ticket"""

        ticket_id = create_ticket_get_id("to update")

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/update",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "ticket_id": ticket_id,
                "subject": "to update (updated)",
                "body": "new body",
                "hidden": True
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), detail_response_schema_template)

    def test_011_close_ticket(self):
        ticket_id = create_ticket_get_id("close me")

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/close",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "ticket_id": ticket_id
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), detail_response_schema_template)

    def test_012_get_liked_ticket(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/liked",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), tickets_list_response_schema_template)

    def test_013_get_bookmarked_ticket(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/bookmarked",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "bookmarks_type": "strangers"
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), tickets_list_response_schema_template)

    def test_014_get_deleted_ticket(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/deleted",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), tickets_list_response_schema_template)

    def test_015_undelete_ticket(self):
        """Delete ticket"""

        ticket_id = create_ticket_get_id("for black list to undelete")

        response = requests.delete(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/delete",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "ticket_id_list": [ticket_id]
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), detail_response_schema_template)

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/undelete",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "ticket_id": ticket_id
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), detail_response_schema_template)

    def test_016_get_full_ticket_history(self):
        """Delete ticket"""

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/full_history",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "ticket_id": TicketsTestCase.first_ticket
            },
            timeout=TIMEOUT
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), test_016_get_full_ticket_history_schema)

    @unittest.skip
    def test_017_get_action_by_id(self):
        """Delete ticket"""

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/get_action",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "action_id": "6522d1207bf20629548622f6"
            },
            timeout=TIMEOUT
        )
