import unittest
import string
import random

import requests

from auth_test import AuthTestCase
from registration_test import RegistrationTestCase

TIMEOUT = 5


def create_ticket_get_id(subject: str) -> int:
    return requests.post(
        "http://127.0.0.1:8080/tickets/create",
        headers={
            "Authorization": f"Bearer {AuthTestCase.access_token}"
        },
        json={
            "creator_id": RegistrationTestCase.user_id,
            "subject": subject,
            "body": "".join(random.sample(string.ascii_letters, 15)),
            "hidden": True if random.randint(0, 9) % 2 == 0 else False,
            "anonymous": True if random.randint(0, 9) % 2 == 0 else False,
            "faculty_id": 1,
            "queue_id": 1,
        },
        timeout=TIMEOUT
    ).json()["ticket_id"]


class TicketsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.first_ticket = 0

    def test_create_ticket(self):
        """Create ticket"""

        response = requests.post(
            "http://127.0.0.1:8080/tickets/create",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "creator_id": RegistrationTestCase.user_id,
                "subject": "".join(random.sample(string.ascii_letters, 5)),
                "body": "".join(random.sample(string.ascii_letters, 15)),
                "hidden": True if random.randint(0, 9) % 2 == 0 else False,
                "anonymous": True if random.randint(0, 9) % 2 == 0 else False,
                "faculty_id": 1,
                "queue_id": 1,
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

        TicketsTestCase.first_ticket = response.json()["ticket_id"]

    def test_delete_ticket(self):
        """Delete ticket"""

        ticket_id = create_ticket_get_id("for black list")

        response = requests.delete(
            "http://127.0.0.1:8080/tickets/delete",
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

    def test_delete_ticket_noexist(self):
        """Delete ticket"""

        response = requests.delete(
            "http://127.0.0.1:8080/tickets/delete",
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

    def test_bookmark_ticket(self):
        """Bookmark ticket"""

        response = requests.post(
            "http://127.0.0.1:8080/tickets/bookmark",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "ticket_id": create_ticket_get_id("for bookmarking")
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_bookmark_ticket_noexist(self):
        """Bookmark ticket"""

        response = requests.post(
            "http://127.0.0.1:8080/tickets/bookmark",
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

    def test_tickets_filter(self):
        response = requests.post(
            "http://127.0.0.1:8080/tickets/ticket_list",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "anonymous": True,
                "hidden": True
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_ticket_detail_view(self):
        ticket_id = create_ticket_get_id("show info about ticket")

        response = requests.post(
            "http://127.0.0.1:8080/tickets/show",
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

    def test_update_ticket(self):
        """Update ticket"""

        ticket_id = create_ticket_get_id("to update")

        response = requests.post(
            "http://127.0.0.1:8080/tickets/update",
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

    def test_close_ticket(self):
        ticket_id = create_ticket_get_id("close me")

        response = requests.post(
            "http://127.0.0.1:8080/tickets/close",
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
