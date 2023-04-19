import unittest
import requests

from auth_test import AuthTestCase


class ProfileTestCase(unittest.TestCase):
    def test_view_profile_without_auth(self):
        """Recv profile data in JSON format"""

        response = requests.post(
            "http://127.0.0.1:8080/profile/",
            timeout=0.1
        )

        self.assertEqual(
            response.status_code,
            401
        )

    def test_view_profile_with_auth(self):
        """Recv profile data in JSON format"""

        response = requests.post(
            "http://127.0.0.1:8080/profile/",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            timeout=0.1
        )

        self.assertEqual(
            response.status_code,
            200
        )
