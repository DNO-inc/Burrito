import unittest

import jsonschema
import requests

from burrito.utils.config_reader import get_config

from .schemas import scheme_test_anon_tickets_list_filter

TIMEOUT = 5


class AnonTestCase(unittest.TestCase):
    def test_anon_tickets_list_filter(self):
        response = requests.post(
            f"{get_config().BURRITO_API_URL}/anon/ticket_list",
            json={
                #                "status": [1, 2, 3],
                "anonymous": False
            },
            timeout=TIMEOUT
        )

        jsonschema.validate(response.json(), scheme_test_anon_tickets_list_filter)
