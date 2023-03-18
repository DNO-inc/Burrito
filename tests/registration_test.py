import string
import random
import unittest
import requests


class RegistrationTestCase(unittest.TestCase):
    """
        This case, test what will be happened if user trying
        to register with existent login.
    """

    @classmethod
    def setUpClass(cls):
        """Generate random login and password"""

        cls.random_login = "".join(random.sample(string.ascii_letters, 5))
        cls.random_password = "".join(random.sample(string.ascii_letters, 5))

    def test_do_registration(self):
        """Make registration"""

        response = requests.post(
            "http://127.0.0.1:8080/registration",
            json={
                "login": RegistrationTestCase.random_login,
                "password": RegistrationTestCase.random_password
            }
        )
        self.assertEqual(response.json().get("code"), "successfully")

    def test_do_registration_with_the_same_login(self):
        """Test case when users try to register with the existent login"""

        response = requests.post(
           "http://127.0.0.1:8080/registration",
            json={
                "login": RegistrationTestCase.random_login,
                "password": RegistrationTestCase.random_password
            }
        )
        self.assertEqual(response.json().get("detail"), "User user with the same login exist.")
