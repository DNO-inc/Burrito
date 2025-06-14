import os
import unittest

import requests

from burrito.utils.config_reader import get_config
from tests.tickets.tickets_test import create_ticket_get_id
from tests.utils import get_access_token

RUNNING_IN_CONTAINER = os.path.exists('/.dockerenv')
SHADOW_FOLDER = "/shadow/" if RUNNING_IN_CONTAINER else "shadow/"


class IOFilesTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_id: None | str = None
        cls.ticket_id: None | int = None

    def test_001_upload_file(self):
        IOFilesTestCase.ticket_id = create_ticket_get_id("lol")

        response = requests.post(
            f"{get_config().BURRITO_API_URL}/iofiles/upload_file",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            data={
                "ticket_id": IOFilesTestCase.ticket_id
            },
            files=[
                ('file_list', ('file2.txt', open(f"{SHADOW_FOLDER}/image.jpg", "rb"), 'image/png')),
                ('file_list', ('file1.txt', open(f"{SHADOW_FOLDER}/test_file", "rb"), 'text/plain'))
            ],
            timeout=3
        )

        self.assertEqual(
            response.status_code,
            200
        )

        IOFilesTestCase.file_id = response.json()["file_id"][0]

    def test_002_get_file(self):

        response = requests.get(
            f"{get_config().BURRITO_API_URL}/iofiles/{IOFilesTestCase.file_id}",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            data={
                "ticket_id": IOFilesTestCase.ticket_id
            },
            timeout=3
        )

        with open(f"{SHADOW_FOLDER}/lol", "wb") as file:
            file.write(response.content)

        self.assertEqual(
            response.status_code,
            200
        )

    def test_003_get_file_ids(self):

        response = requests.post(
            f"{get_config().BURRITO_API_URL}/iofiles/get_file_ids",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            data={
                "ticket_id": IOFilesTestCase.ticket_id
            },
            timeout=0.5
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_004_delete_file(self):

        response = requests.post(
            f"{get_config().BURRITO_API_URL}/iofiles/delete_file",
            headers={
                "Authorization": f"Bearer {get_access_token()}"
            },
            data={
                "file_id": IOFilesTestCase.file_id
            },
            timeout=0.5
        )

        self.assertEqual(
            response.status_code,
            200
        )
