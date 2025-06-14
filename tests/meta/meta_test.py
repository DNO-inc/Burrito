import unittest

import jsonschema
import requests

from burrito.utils.config_reader import get_config
from tests.utils import get_access_token

from .schemas import *

TIMEOUT = 5


class MetaTestCase(unittest.TestCase):
    def test_001_roles(self):
        response = requests.get(
            f"{get_config().BURRITO_API_URL}/meta/get_roles",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=TIMEOUT
        )

        jsonschema.validate(response.json(), test_001_roles_schema)

    def test_002_role_permissions(self):
        response = requests.get(
            f"{get_config().BURRITO_API_URL}/meta/get_role_permissions",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=TIMEOUT
        )

        jsonschema.validate(response.json(), test_002_role_permissions_schema)

    def test_get_statuses_list(self):
        response = requests.get(
            f"{get_config().BURRITO_API_URL}/meta/get_statuses",
            timeout=TIMEOUT
        )

        jsonschema.validate(response.json(), test_get_statuses_list_schema)

    def test_groups_list(self):
        response = requests.get(
            f"{get_config().BURRITO_API_URL}/meta/get_groups",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=TIMEOUT
        )

        jsonschema.validate(response.json(), test_groups_list_schema)

    def test_faculties_list(self):
        response = requests.get(
            f"{get_config().BURRITO_API_URL}/meta/get_faculties",
            timeout=TIMEOUT
        )

        jsonschema.validate(response.json(), test_faculties_list_schema)

    def test_queues_list(self):
        response = requests.post(
            f"{get_config().BURRITO_API_URL}/meta/get_queues",
            json={
                "faculty": 414
            },
            timeout=TIMEOUT
        )

        jsonschema.validate(response.json(), test_queues_list_schema)

    def test_queues_list_with_wrong_faculty(self):
        response = requests.post(
            f"{get_config().BURRITO_API_URL}/meta/get_queues",
            json={
                "faculty": 999999999
            },
            timeout=TIMEOUT
        )

        jsonschema.validate(response.json(), test_queues_list_with_wrong_faculty_schema)

    def test_get_admin_list(self):
        response = requests.post(
            f"{get_config().BURRITO_API_URL}/meta/get_admins",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            timeout=TIMEOUT
        )

        jsonschema.validate(response.json(), test_get_admin_list_schema)
