import unittest

import requests

from auth_test import AuthTestCase

from burrito.utils.config_reader import get_config


class IOFilesTestCase(unittest.TestCase):
    def test_upload_file(self):

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/iofiles/upload_file",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            data={
                "ticket_id": 1
            },
            files=[
                ('file_list', ('file1.txt', open("tests/test_file", "rb"), 'text/plain')),
                ('file_list', ('file2.txt', open("tests/test_file", "rb"), 'text/plain'))
            ],
            timeout=0.5
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_get_file(self):

        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/iofiles/get_files",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            data={
                "ticket_id": 1
            },
            timeout=0.5
        )

        self.assertEqual(
            response.status_code,
            200
        )
