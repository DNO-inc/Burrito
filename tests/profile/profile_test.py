import string
import random
import unittest

import requests
import jsonschema

from burrito.utils.config_reader import get_config

from tests.utils import get_access_token, setup_test_user

from .schemas import *


class ProfileTestCase(unittest.TestCase):
    def test_view_profile_noexist(self):
        """Recv profile data in JSON format"""

        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/profile/1000000",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=0.5
        )

        assert response.status_code == 404

        _response_schema = {
            "type": "object",
            "properties": {
                "detail": {"type": "string"}
            }
        }

        jsonschema.validate(response.json(), _response_schema)

    def test_view_profile_without_auth_with_id(self):
        """Recv profile data in JSON format"""

        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/profile/{setup_test_user()}",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=0.5
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), profile_view_schema_template)

    def test_view_profile_with_auth_with_id(self):
        """Recv profile data in JSON format"""

        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/profile/{setup_test_user()}",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=0.5
        )

        assert response.status_code == 200

        jsonschema.validate(response.json(), profile_view_schema_template)

    def test_update_profile_without_auth(self):
        """Update profile data"""

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/profile/update",
            timeout=0.5
        )

        assert response.status_code == 401

        _response_schema = {
            "type": "object",
            "properties": {
                "detail": {"type": "string"}
            }
        }

        jsonschema.validate(response.json(), _response_schema)

    def test_update_profile_with_auth(self):
        """Update profile data"""

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/profile/update",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            json={
                "firstname": "".join(random.sample(string.ascii_letters, 5)) if random.randint(0, 10) % 2 == 0 else None,
                "lastname": "".join(random.sample(string.ascii_letters, 5)) if random.randint(0, 10) % 2 == 0 else None,
                "email": "".join(random.sample(string.ascii_letters, 5)) if random.randint(0, 10) % 2 == 0 else None,
                "phone": "".join(random.sample(string.ascii_letters, 5)) if random.randint(0, 10) % 2 == 0 else None,
                "faculty": random.choice([414, 1675]),
                "group": random.choice([1003254, 1003565]),
            },
            timeout=0.5
        )

        assert response.status_code == 200

        _response_schema = {
            "type": "object",
            "properties": {
                "detail": {"type": "string"}
            }
        }

        jsonschema.validate(response.json(), _response_schema)
