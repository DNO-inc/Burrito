import unittest
import requests

from burrito.utils.config_reader import get_config
from utils.exceptions_tool import check_error


TIMEOUT = 5


class AnonTestCase(unittest.TestCase):
    def test_anon_tickets_list_filter(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/anon/ticket_list",
            json={
                "status": [1, 2, 3],
                "anonymous": True
            },
            timeout=TIMEOUT
        )

        check_error(
            self.assertEqual,
            {
                "first": response.status_code,
                "second": 200
            },
            response
        )
