import unittest
import requests

TIMEOUT = 5


class AnonTestCase(unittest.TestCase):
    def test_anon_tickets_list_filter(self):
        response = requests.post(
            "http://127.0.0.1:8080/anon/ticket_list",
            json={
                "anonymous": False
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )
