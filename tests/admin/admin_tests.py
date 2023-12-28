import random

import unittest
import requests

from tests.auth.auth_test import AuthTestCase
from tests.tickets.tickets_test import TicketsTestCase

from burrito.utils.config_reader import get_config
from utils.exceptions_tool import check_error


TIMEOUT = 10


class AdminTestCase(unittest.TestCase):
    def test_001_admin_update_ticket(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/admin/tickets/update",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "ticket_id": TicketsTestCase.first_ticket,
                "status": random.choice([1, 2, 3, 4, 5]),
                "faculty": 1
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

    def test_002_admin_ticket_list_view(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/admin/tickets/ticket_list",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "scope": 'Reports',
                "queue": [2],
                "status": [6],
                "hidden": True,
                "anonymous": True
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

    def test_003_admin_ticket_detail_view(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/admin/tickets/show",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "ticket_id": TicketsTestCase.first_ticket
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

    @unittest.skip
    def test_004_admin_delete_ticket(self):
        response = requests.delete(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/admin/tickets/delete",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "ticket_id": TicketsTestCase.first_ticket - 1
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
