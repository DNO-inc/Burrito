import random
import string
import unittest

import jsonschema
import requests

from burrito.utils.config_reader import get_config

TIMEOUT = 5


def make_user_registration(
    login: str = "".join(random.sample(string.ascii_letters, 5)),
    password: str = "".join(random.sample(string.ascii_letters, 8)),
    group: int = 1003254,
    division_id: int = 414
):
    response = requests.post(
        f"{get_config().BURRITO_API_URL}/registration/",
        json={
            "firstname": "firstname",
            "lastname": "lastname",
            "login": login,
            "password": password,
            "email": "".join(random.sample(string.ascii_letters, 5)),
            "group": group,
            "division": division_id
        },
        timeout=TIMEOUT
    )

    assert response.status_code == 200

    _response_schema = {
        "type": "object",
        "properties": {
            "status_id": {"type": "string"}
        }
    }

    jsonschema.validate(response.json(), _response_schema)


class RegistrationTestCase(unittest.TestCase):
    """
        This case, test what will be happened if user trying
        to register with existent login.
    """
    user_id = 1

    @classmethod
    def setUpClass(cls):
        """Generate random login and password"""

        cls.random_login = "".join(random.sample(string.ascii_letters, 5))
        cls.random_password = "".join(random.sample(string.ascii_letters, 8))
        cls.user_id: int = 1

    def test_do_registration(self):
        """Make registration"""

        make_user_registration(
            login=RegistrationTestCase.random_login,
            password=RegistrationTestCase.random_password,
        )

    @unittest.skip
    def test_do_registration_with_invalid_login(self):
        """make registration with invalid datas"""

        make_user_registration(
            login=".",
            password=RegistrationTestCase.random_password
        )

    @unittest.skip
    def test_do_registration_with_invalid_password(self):
        """make registration with invalid datas"""

        make_user_registration(
            login="".join(random.sample(string.ascii_letters, 5)),
            password="."
        )

    @unittest.skip
    def test_do_registration_with_invalid_group(self):
        """make registration with invalid datas"""

        make_user_registration(
            group="hello_man_11"
        )

    @unittest.skip
    def test_do_registration_with_invalid_division(self):
        """make registration with invalid datas"""

        make_user_registration(
            division_id="hello_man_11"
        )

    @unittest.skip
    def test_do_registration_with_the_same_login(self):
        """Test case when users try to register with the existent login"""

        make_user_registration(
            login=RegistrationTestCase.random_login,
            password=RegistrationTestCase.random_password
        )
