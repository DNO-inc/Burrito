import string
import random
import unittest
import requests

from burrito.utils.config_reader import get_config
from utils.exceptions_tool import check_error


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
            "group": group,
            "faculty": faculty
        },
        timeout=TIMEOUT
    )

    if response.json().get("user_id"):
        return response.json().get("user_id")

    return response


class RegistrationTestCase(unittest.TestCase):
    """
        This case, test what will be happened if user trying
        to register with existent login.
    """

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

        check_error(
            self.assertIsInstance,
            {
                "obj": user_data,
                "cls": int
            },
            user_data
        )

        RegistrationTestCase.user_id = user_data

    def test_do_registration_with_invalid_login(self):
        """make registration with invalid datas"""

        user_data = make_user_registration(
            login=".",
            password=RegistrationTestCase.random_password
        )

        check_error(
            self.assertEqual,
            {
                "first": user_data.status_code,
                "second": 422
            }
        )

    def test_do_registration_with_invalid_password(self):
        """make registration with invalid datas"""

        user_data = make_user_registration(
            login="".join(random.sample(string.ascii_letters, 5)),
            password="."
        )

        check_error(
            self.assertEqual,
            {
                "first": user_data.status_code,
                "second": 422
            }
        )

    def test_do_registration_with_invalid_group(self):
        """make registration with invalid datas"""

        user_data = make_user_registration(
            group="hello_man_11"
        )

        check_error(
            self.assertEqual,
            {
                "first": user_data.status_code,
                "second": 422
            }
        )

    def test_do_registration_with_invalid_faculty(self):
        """make registration with invalid datas"""

        user_data = make_user_registration(
            faculty="hello_man_11"
        )

        check_error(
            self.assertEqual,
            {
                "first": user_data.status_code,
                "second": 422
            }
        )

    def test_do_registration_with_the_same_login(self):
        """Test case when users try to register with the existent login"""

        user_data = make_user_registration(
            login=RegistrationTestCase.random_login,
            password=RegistrationTestCase.random_password
        )

        check_error(
            self.assertEqual,
            {
                "first": user_data.status_code,
                "second": 422
            }
        )
