import unittest

import requests

from tests.tickets.tickets_test import create_ticket_get_id
from tests.utils import get_access_token
from burrito.utils.config_reader import get_config



class IOFilesTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_id: None | str = None
        cls.ticket_id: None | int = None

    def test_001_upload_file(self):
        IOFilesTestCase.ticket_id = create_ticket_get_id("lol")

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/iofiles/upload_file",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            data={
                "ticket_id": IOFilesTestCase.ticket_id
            },
            files=[
                ('file_list', ('file2.txt', open("shadow/image.jpg", "rb"), 'image/png')),
                ('file_list', ('file1.txt', open("shadow/test_file", "rb"), 'text/plain'))
            ],
            timeout=0.5
        )

        self.assertEqual(
            response.status_code,
            200
        )

        IOFilesTestCase.file_id = response.json()["file_id"][0]

    def test_002_get_file(self):

        response = requests.get(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/iofiles/{IOFilesTestCase.file_id}",
            headers={
               "Authorization": f"Bearer {get_access_token()}"
            },
            data={
                "ticket_id": IOFilesTestCase.ticket_id
            },
            timeout=0.5
        )

        with open("shadow/lol", "wb") as file:
            file.write(response.content)

        self.assertEqual(
            response.status_code,
            200
        )

    def test_003_get_file_ids(self):

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/iofiles/get_file_ids",
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
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/iofiles/delete_file",
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
