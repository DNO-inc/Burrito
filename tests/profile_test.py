import string
import random
import unittest

import requests

from auth_test import AuthTestCase
from registration_test import RegistrationTestCase

from burrito.utils.config_reader import get_config
from utils.exceptions_tool import check_error


class ProfileTestCase(unittest.TestCase):
    def test_view_profile_noexist(self):
        """Recv profile data in JSON format"""

        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/profile/1000000",
            timeout=0.5
        )

        check_error(
            self.assertEqual,
            {
                "first": response.status_code,
                "second": 404
            },
            response
        )

    def test_view_profile_without_auth_with_id(self):
        """Recv profile data in JSON format"""

        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/profile/{RegistrationTestCase.user_id}",
            timeout=0.5
        )

        check_error(
            self.assertEqual,
            {
                "first": response.status_code,
                "second": 200
            },
            response
        )

    def test_view_profile_with_auth_with_id(self):
        """Recv profile data in JSON format"""

        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/profile/{RegistrationTestCase.user_id}",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            timeout=0.5
        )

        check_error(
            self.assertEqual,
            {
                "first": response.status_code,
                "second": 200
            },
            response
        )

    def test_update_profile_without_auth(self):
        """Update profile data"""

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/profile/update",
            timeout=0.5
        )

        self.assertEqual(
            response.status_code,
            401
        )

    def test_update_profile_with_auth(self):
        """Update profile data"""

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/profile/update",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "firstname": "".join(random.sample(string.ascii_letters, 5)) if random.randint(0, 10) % 2 == 0 else None,
                "lastname": "".join(random.sample(string.ascii_letters, 5)) if random.randint(0, 10) % 2 == 0 else None,
                "email": "".join(random.sample(string.ascii_letters, 5)) if random.randint(0, 10) % 2 == 0 else None,
                "phone": "".join(random.sample(string.ascii_letters, 5)) if random.randint(0, 10) % 2 == 0 else None,
                "faculty": random.choice([1, 2]),
                "group": random.choice([1, 2]),
            },
            timeout=0.5
        )

        check_error(
            self.assertEqual,
            {
                "first": response.status_code,
                "second": 200
            },
            response
        )
