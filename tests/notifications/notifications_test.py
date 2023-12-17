import unittest
import requests
import jsonschema

from burrito.utils.config_reader import get_config

from .schemas import *


TIMEOUT = 5
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2dpdGh1Yi5jb20vRE5PLWluYyIsInN1YiI6ImF1dGgiLCJleHAiOjE3MDI3NzIyNzEsImlhdCI6MTcwMjc2MjI3MSwianRpIjoiOTEwMTY3OWNiYTEwNDdhY2FlMzA1YTg5MzFlYzIyZmIiLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwidXNlcl9pZCI6MSwicm9sZSI6IkFETUlOIiwiYnVycml0b19zYWx0IjoiNWIwOTE1Mjc0NjRiNWU0OTVmMTY3ZmI3M2M4Y2U3MDJiYzVhOTgzMDg4NzEwYTM3MjdkMDYxMzg0NTYzYmEyYTFjMjcxYTI2NzkyMGZkYTlhNTU2NWE3NWFhYjQ3NDA0NDc4N2Y5OTAxYjNmMjY1MDhkNDI2OTllMWIyOGIyMGQifQ.Dry9cK53I7rHoSrM8VXVs12pqTGQ57kR5VeIG9D8y2s"


class NotificationsTestCase(unittest.TestCase):
    def test_001_get_notifications(self):
        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/notifications/offline",
            headers={
               "Authorization": f"Bearer {access_token}"
            },
            timeout=TIMEOUT
        )

        jsonschema.validate(response.json(), test_001_get_notifications_schema)
