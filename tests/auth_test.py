import unittest
import requests

from registration_test import RegistrationTestCase

from burrito.utils.config_reader import get_config
from utils.exceptions_tool import check_error


def do_auth():
    response = requests.post(
        f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/auth/password/login",
        json={
            "login": RegistrationTestCase.random_login,
            "password": RegistrationTestCase.random_password
        },
        timeout=5
    )
    return response.status_code, response.json()


class AuthTestCase(unittest.TestCase):
    """Test authentication system"""

    @classmethod
    def setUpClass(cls):
        cls.access_token: None | str = None
        cls.refresh_token: None | str = None

    def test_001_do_password_auth(self):
        """
            Login user in rest API using login and password.
            Recv token to use in the next authentications.
        """

        result: tuple[int, dict] = do_auth()

        access_token = result[1].get("access_token")
        AuthTestCase.access_token = access_token

        refresh_token = result[1].get("refresh_token")
        AuthTestCase.refresh_token = refresh_token

        check_error(
            self.assertEqual,
            {
                "first": result[0],
                "second": 200
            },
            result[1]
        )

#    @unittest.skip
    def test_002_refresh_access_token(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/auth/token/refresh",
            headers={
               "Authorization": f"Bearer {AuthTestCase.refresh_token}"
            },
            timeout=5
        )
        check_error(
            self.assertEqual,
            {
                "first": response.status_code,
                "second": 200
            },
            response
        )
        AuthTestCase.access_token = response.json()["access_token"]

    def test_003_delete_token_pare(self):
        result: tuple[int, dict] = do_auth()

        refresh_token = result[1].get("refresh_token")
        print(refresh_token)
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/auth/token/delete",
            headers={
               "Authorization": f"Bearer {refresh_token}"
            },
            timeout=5
        )

        check_error(
            self.assertEqual,
            {
                "first": response.status_code,
                "second": 200
            },
            response
        )
