import unittest
import requests

from burrito.utils.config_reader import get_config


class AboutTestCase(unittest.TestCase):
    def test_check_version(self):
        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/about/version",
            timeout=0.1
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_check_updates(self):
        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/about/updates",
            timeout=0.1
        )
        print(response.json())
        self.assertEqual(
            response.status_code,
            200
        )

    def test_check_team(self):
        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/about/team",
            timeout=0.1
        )
        print(response.json())
        self.assertEqual(
            response.status_code,
            200
        )
