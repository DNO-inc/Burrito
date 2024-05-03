import unittest
import requests
import jsonschema

from burrito.utils.config_reader import get_config

from tests.utils import get_token_pare

from .schemas import *


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

        result = get_token_pare()

        access_token = result["access_token"]
        AuthTestCase.access_token = access_token

        refresh_token = result["refresh_token"]
        AuthTestCase.refresh_token = refresh_token

#    @unittest.skip
    def test_002_refresh_access_token(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/auth/token/refresh",
            headers={
               "Authorization": f"Bearer {AuthTestCase.refresh_token}"
            },
            timeout=5
        )

        self.assertEqual(response.status_code, 200, response.json())

        jsonschema.validate(response.json(), test_002_refresh_access_token_schema)
        AuthTestCase.access_token = response.json()["access_token"]

    def test_003_delete_token_pare(self):
        result = get_token_pare()

        refresh_token = result["refresh_token"]

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/auth/token/delete",
            headers={
               "Authorization": f"Bearer {refresh_token}"
            },
            timeout=5
        )

        self.assertEqual(response.status_code, 200, response.json())
