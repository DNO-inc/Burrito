import unittest
import requests

from burrito.utils.config_reader import get_config
from utils.exceptions_tool import check_error

from auth_test import AuthTestCase


TIMEOUT = 5


class NotificationsTestCase(unittest.TestCase):
    def test_001_get_notifications(self):
        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/notifications/",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
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