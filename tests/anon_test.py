import unittest
import requests

from burrito.utils.config_reader import get_config


TIMEOUT = 5


class AnonTestCase(unittest.TestCase):
    def test_anon_tickets_list_filter(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/anon/ticket_list",
            json={
                "status": [1, 2],
#                "anonymous": True
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )
