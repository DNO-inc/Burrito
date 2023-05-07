import unittest
import requests
import string
import random

from auth_test import AuthTestCase
from registration_test import RegistrationTestCase


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
                "user_id": RegistrationTestCase.user_id
            },
            timeout=0.1
        )

        self.assertEqual(
            response.status_code,
            200
        )

        TicketsTestCase.first_ticket = response.json()["ticket_id"]

#    @unittest.skip
    def test_delete_ticket(self):
        """Delete ticket"""

        response = requests.delete(
            "http://127.0.0.1:8080/tickets/delete",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "ticket_id": TicketsTestCase.first_ticket
            },
            timeout=0.1
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
                "ticket_id": TicketsTestCase.first_ticket
            },
            timeout=0.1
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_update_ticket(self):
        """Update ticket"""

        ticket_id = requests.post(
            "http://127.0.0.1:8080/tickets/create",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "creator_id": RegistrationTestCase.user_id,
                "subject": "to update",
                "body": "".join(random.sample(string.ascii_letters, 15)),
                "hidden": False,
                "anonymous": False,
                "faculty_id": 1,
                "queue_id": 1,
                "user_id": RegistrationTestCase.user_id
            },
            timeout=0.1
        ).json()["ticket_id"]

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
            timeout=0.1
        )

        self.assertEqual(
            response.status_code,
            200
        )
