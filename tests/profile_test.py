import string
import random
import unittest

import requests

from auth_test import AuthTestCase
from registration_test import RegistrationTestCase


class ProfileTestCase(unittest.TestCase):
    def test_view_profile_without_auth_with_id(self):
        """Recv profile data in JSON format"""

        response = requests.post(
            "http://127.0.0.1:8080/profile/",
            json={
                "user_id": RegistrationTestCase.user_id
            },
            timeout=0.5
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_view_profile_without_auth_without_id(self):
        """Recv profile data in JSON format"""

        response = requests.post(
            "http://127.0.0.1:8080/profile/",
            json={},
            timeout=0.5
        )

        self.assertEqual(
            response.status_code,
            401
        )

    def test_view_profile_with_auth_with_id(self):
        """Recv profile data in JSON format"""

        response = requests.post(
            "http://127.0.0.1:8080/profile/",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "user_id": RegistrationTestCase.user_id
            },
            timeout=0.5
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_view_profile_with_auth_without_id(self):
        """Recv profile data in JSON format"""

        response = requests.post(
            "http://127.0.0.1:8080/profile/",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={},
            timeout=0.5
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_update_profile_without_auth(self):
        """Update profile data"""

        response = requests.post(
            "http://127.0.0.1:8080/profile/update",
            json={},
            timeout=0.5
        )

        self.assertEqual(
            response.status_code,
            401
        )

    def test_update_profile_with_auth(self):
        """Update profile data"""

        response = requests.post(
            "http://127.0.0.1:8080/profile/update",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "firstname": "".join(random.sample(string.ascii_letters, 5)) if random.randint(0, 10) % 2 == 0 else None,
                "lastname": "".join(random.sample(string.ascii_letters, 5)) if random.randint(0, 10) % 2 == 0 else None,
                "email": "".join(random.sample(string.ascii_letters, 5)) if random.randint(0, 10) % 2 == 0 else None,
                "phone": "".join(random.sample(string.ascii_letters, 5)) if random.randint(0, 10) % 2 == 0 else None,
                "faculty": random.choice(["EliT", "Biem"]),
                "group": random.choice(["IT-11", "LOL-11"]),
            },
            timeout=0.5
        )

        self.assertEqual(
            response.status_code,
            200
        )
