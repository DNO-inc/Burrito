import unittest

import jsonschema
import requests

from burrito.utils.config_reader import get_config
from tests.utils import get_access_token

from .schemas import *


class StatisticTestCase(unittest.TestCase):
    def test_activity_statistic(self):
        """Recv profile data in JSON format"""

        response = requests.get(
            f"{get_config().BURRITO_API_URL}/statistic/activity_summary",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=0.5
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), statistic_activity_schema)

    def test_division_statistic(self):
        """Recv profile data in JSON format"""

        response = requests.get(
            f"{get_config().BURRITO_API_URL}/statistic/divisions",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=0.5
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), statistic_division_schema)

    def test_period_statistic(self):
        """Recv profile data in JSON format"""

        response = requests.get(
            f"{get_config().BURRITO_API_URL}/statistic/period",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=0.5
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), statistic_period_schema)
