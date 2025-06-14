import unittest

import jsonschema
import requests

from burrito.utils.config_reader import get_config
from tests.utils import get_access_token

from .schemas import *

TIMEOUT = 5


class NotificationsTestCase(unittest.TestCase):
    def test_001_get_notifications(self):
        response = requests.get(
            f"{get_config().BURRITO_API_URL}/notifications/offline",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=TIMEOUT
        )

        jsonschema.validate(response.json(), test_001_get_notifications_schema)
