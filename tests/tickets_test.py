import unittest
import string
import random

import requests

from auth_test import AuthTestCase

from burrito.utils.config_reader import get_config


TIMEOUT = 10


def create_ticket_get_id(subject: str) -> int:
    return requests.post(
        f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/create",
        headers={
            "Authorization": f"Bearer {AuthTestCase.access_token}"
        },
        json={
            "subject": subject,
            "body": "".join([random.choice(string.ascii_letters) for i in range(700)]),
            "hidden": True if random.randint(0, 9) % 2 == 0 else False,
            "anonymous": True if random.randint(0, 9) % 2 == 0 else False,
            "queue": "questions",
            "faculty": random.choice(["EliT", "Biem"]),
        },
        timeout=TIMEOUT
    ).json()["ticket_id"]


class TicketsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.first_ticket = 0

    def test_001_create_ticket(self):
        """Create ticket"""

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/create",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "subject": "".join(random.sample(string.ascii_letters, 5)),
                "body": "".join([random.choice(string.ascii_letters) for i in range(700)]),
                "hidden": True if random.randint(0, 9) % 2 == 0 else False,
                "anonymous": True if random.randint(0, 9) % 2 == 0 else False,
                "queue": "questions",
                "faculty": random.choice(["EliT", "Biem"]),
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

        TicketsTestCase.first_ticket = response.json()["ticket_id"]

    def test_002_delete_ticket(self):
        """Delete ticket"""

        ticket_id = create_ticket_get_id("for black list")

        response = requests.delete(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/delete",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "ticket_id": ticket_id
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_003_delete_ticket_noexist(self):
        """Delete ticket"""

        response = requests.delete(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/delete",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "ticket_id": TicketsTestCase.first_ticket + 123456
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_004_like_ticket(self):
        """Delete ticket"""

        ticket_id = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/create",
            headers={
                "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "subject": "to like",
                "body": "".join([random.choice(string.ascii_letters) for i in range(700)]),
                "hidden": False,
                "anonymous": True if random.randint(0, 9) % 2 == 0 else False,
                "queue": "questions",
                "faculty": random.choice(["EliT", "Biem"]),
            },
            timeout=TIMEOUT
        ).json()["ticket_id"]

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/like",
            headers={
                "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "ticket_id": ticket_id
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_005_like_ticket_noexist(self):
        """Delete ticket"""

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/like",
            headers={
                "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "ticket_id": TicketsTestCase.first_ticket + 123456
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_006_bookmark_ticket(self):
        """Bookmark ticket"""

        ticket_id = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/create",
            headers={
                "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "subject": "to bookmark",
                "body": "".join([random.choice(string.ascii_letters) for i in range(700)]),
                "hidden": False,
                "anonymous": True if random.randint(0, 9) % 2 == 0 else False,
                "queue": "questions",
                "faculty": random.choice(["EliT", "Biem"]),
            },
            timeout=TIMEOUT
        ).json()["ticket_id"]

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/bookmark",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "ticket_id": ticket_id
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_007_bookmark_ticket_noexist(self):
        """Bookmark ticket"""

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/bookmark",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "ticket_id": TicketsTestCase.first_ticket + 123456
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_008_tickets_filter(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/ticket_list",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "anonymous": True,
                "hidden": False,
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_009_ticket_detail_view(self):
        ticket_id = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/create",
            headers={
                "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "subject": "show info about ticket",
                "body": "".join([random.choice(string.ascii_letters) for i in range(300)]),
                "hidden": False,
                "anonymous": False,
                "queue": "questions",
                "faculty": "EliT",
            },
            timeout=TIMEOUT
        ).json()["ticket_id"]

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/show",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "ticket_id": ticket_id
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_010_update_ticket(self):
        """Update ticket"""

        ticket_id = create_ticket_get_id("to update")

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/update",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "ticket_id": ticket_id,
                "subject": "to update (updated)",
                "body": "new body",
                "hidden": True
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_011_close_ticket(self):
        ticket_id = create_ticket_get_id("close me")

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/close",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "ticket_id": ticket_id
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_012_get_liked_ticket(self):
        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/liked",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={},
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_013_get_bookmarked_ticket(self):
        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/tickets/bookmarked",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={},
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )
