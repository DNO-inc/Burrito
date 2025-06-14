import unittest

import jsonschema
import requests

from burrito.utils.config_reader import get_config

from .schemas import (
    test_check_team_schema,
    test_check_updates_schema,
    test_check_version_schema,
)

TIMEOUT = 5


class AboutTestCase(unittest.TestCase):
    def test_check_version(self):
        response = requests.get(
            f"{get_config().BURRITO_API_URL}/about/version",
            timeout=TIMEOUT
        )

        jsonschema.validate(response.json(), test_check_version_schema)

    def test_check_updates(self):
        response = requests.get(
            f"{get_config().BURRITO_API_URL}/about/updates",
            timeout=TIMEOUT
        )

        jsonschema.validate(response.json(), test_check_updates_schema)

    def test_check_team(self):
        response = requests.get(
            f"{get_config().BURRITO_API_URL}/about/team",
            timeout=TIMEOUT
        )

        jsonschema.validate(response.json(), test_check_team_schema)
