import unittest

import requests
import jsonschema

from burrito.utils.config_reader import get_config

from tests.utils import get_access_token

from .schemas import *


class StatisticTestCase(unittest.TestCase):
    def test_activity_statistic(self):
        """Recv profile data in JSON format"""

        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/statistic/activity_summary",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=0.5
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), statistic_activity_schema)

    def test_faculty_statistic(self):
        """Recv profile data in JSON format"""

        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/statistic/faculties",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=0.5
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), statistic_faculty_schema)

    def test_period_statistic(self):
        """Recv profile data in JSON format"""

        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/statistic/period",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=0.5
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), statistic_period_schema)
