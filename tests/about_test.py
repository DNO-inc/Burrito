import unittest
import requests


class AboutTestCase(unittest.TestCase):
    def test_check_version(self):
        response = requests.get(
            "http://127.0.0.1:8080/about/version",
            timeout=0.1
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_check_updates(self):
        response = requests.get(
            "http://127.0.0.1:8080/about/updates",
            timeout=0.1
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_check_team(self):
        response = requests.get(
            "http://127.0.0.1:8080/about/team",
            timeout=0.1
        )

        self.assertEqual(
            response.status_code,
            200
        )
