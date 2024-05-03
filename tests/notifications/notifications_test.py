import unittest
import requests
import jsonschema

from burrito.utils.config_reader import get_config
from tests.utils import get_access_token

from .schemas import *


TIMEOUT = 5


class NotificationsTestCase(unittest.TestCase):
    def test_001_get_notifications(self):
        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/notifications/offline",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=TIMEOUT
        )

        self.assertEqual(response.status_code, 200, response.json())

        jsonschema.validate(response.json(), test_001_get_notifications_schema)
