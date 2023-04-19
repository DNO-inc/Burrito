import unittest
import requests

from registration_test import RegistrationTestCase


class AuthTestCase(unittest.TestCase):
    """Test authentication system"""

    @classmethod
    def setUpClass(cls):
        cls.access_token: None | str = None

    def test_do_password_auth(self):
        """
            Login user in rest API using login and password.
            Recv token to use in the next authentications.
        """

        response = requests.post(
            "http://127.0.0.1:8080/auth/password/login",
            json={
                "login": RegistrationTestCase.random_login,
                "password": RegistrationTestCase.random_password
            },
            timeout=0.1
        )
        access_token = response.json().get("access_token")

        AuthTestCase.access_token = access_token
        self.assertIsNotNone(access_token)
