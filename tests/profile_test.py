import unittest
import requests

from auth_test import AuthTestCase


class ProfileTestCase(unittest.TestCase):
    def test_view_profile_without_auth(self):
        """Recv profile data in JSON format"""

        self.assertEqual(
            requests.post(
                "http://127.0.0.1:8080/profile"
            ).json().get("detail"),
            "Missing Authorization Header"
        )

    def test_view_profile_with_auth(self):
        """Recv profile data in JSON format"""

        self.assertNotEqual(
            requests.post(
                "http://127.0.0.1:8080/profile",
                headers={
                    "Authorization": f"Bearer {AuthTestCase.access_token}"
                }
            ).json().get("detail"),
            "Missing Authorization Header"
        )
