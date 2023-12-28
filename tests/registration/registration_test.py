import string
import random
import unittest
import requests

import jsonschema

from burrito.utils.config_reader import get_config

TIMEOUT = 5


def make_user_registration(
    login: str = "".join(random.sample(string.ascii_letters, 5)),
    password: str = "".join(random.sample(string.ascii_letters, 8)),
    group: int = 1003254,
    faculty: int = 414
):
    response = requests.post(
        f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/registration/",
        json={
            "firstname": "firstname",
            "lastname": "lastname",
            "login": login,
            "password": password,
            "email": "".join(random.sample(string.ascii_letters, 5)),
            "group": group,
            "faculty": faculty
        },
        timeout=TIMEOUT
    )

    assert response.status_code == 200

    _response_schema = {
        "type": "object",
        "properties": {
            "status": {"type": "string"}            
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

        user_data = make_user_registration(
            login=RegistrationTestCase.random_login,
            password=RegistrationTestCase.random_password,
        )

        RegistrationTestCase.user_id = user_data

    @unittest.skip
    def test_do_registration_with_invalid_login(self):
        """make registration with invalid datas"""

        user_data = make_user_registration(
            login=".",
            password=RegistrationTestCase.random_password
        )

    @unittest.skip
    def test_do_registration_with_invalid_password(self):
        """make registration with invalid datas"""

        user_data = make_user_registration(
            login="".join(random.sample(string.ascii_letters, 5)),
            password="."
        )

    @unittest.skip
    def test_do_registration_with_invalid_group(self):
        """make registration with invalid datas"""

        user_data = make_user_registration(
            group="hello_man_11"
        )

    @unittest.skip
    def test_do_registration_with_invalid_faculty(self):
        """make registration with invalid datas"""

        user_data = make_user_registration(
            faculty="hello_man_11"
        )

    @unittest.skip
    def test_do_registration_with_the_same_login(self):
        """Test case when users try to register with the existent login"""

        user_data = make_user_registration(
            login=RegistrationTestCase.random_login,
            password=RegistrationTestCase.random_password
        )
