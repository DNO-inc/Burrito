import unittest
import requests

TIMEOUT = 5


class MetaTestCase(unittest.TestCase):
    def test_get_statuses_list(self):
        response = requests.get(
            "http://127.0.0.1:8080/meta/get_statuses",
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_groups_list(self):
        response = requests.get(
            "http://127.0.0.1:8080/meta/get_groups",
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_faculties_list(self):
        response = requests.get(
            "http://127.0.0.1:8080/meta/get_faculties",
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_queues_list(self):
        response = requests.post(
            "http://127.0.0.1:8080/meta/get_queues",
            json={
                "faculty": "EliT"
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_queues_list_with_wrong_faculty(self):
        response = requests.post(
            "http://127.0.0.1:8080/meta/get_queues",
            json={
                "faculty": "NotEliT"
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            403
        )
