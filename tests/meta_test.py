import unittest
import requests

from burrito.utils.config_reader import get_config


TIMEOUT = 5


class MetaTestCase(unittest.TestCase):
    def test_get_statuses_list(self):
        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/meta/get_statuses",
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_groups_list(self):
        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/meta/get_groups",
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_faculties_list(self):
        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/meta/get_faculties",
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_queues_list(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/meta/get_queues",
            json={
                "faculty": 1
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_queues_list_with_wrong_faculty(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/meta/get_queues",
            json={
                "faculty": "NotEliT"
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            422
        )
