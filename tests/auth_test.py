import unittest
import requests

from registration_test import RegistrationTestCase

from burrito.utils.config_reader import get_config


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
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/auth/password/login",
            json={
                "login": RegistrationTestCase.random_login,
                "password": RegistrationTestCase.random_password
            },
            timeout=5
        )

        access_token = response.json().get("access_token")
        AuthTestCase.access_token = access_token

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(access_token)
