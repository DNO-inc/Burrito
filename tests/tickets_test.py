import unittest
import requests
import string
import random

from auth_test import AuthTestCase
from registration_test import RegistrationTestCase


class TicketsTestCase(unittest.TestCase):
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
                "hidden": False,
                "anonymous": True,
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
