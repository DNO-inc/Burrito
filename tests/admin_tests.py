import random

import unittest
import requests

from auth_test import AuthTestCase
from tickets_test import TicketsTestCase

from burrito.utils.config_reader import get_config


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
                "status": random.choice(
                    ["ACCEPTED", "OPEN", "WAITING", "REJECTED", "CLOSE", None]
                )
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_002_admin_ticket_list_view(self):
        response = requests.post(
            f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/admin/tickets/ticket_list",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "hidden": True,
                "anonymous": True
            },
            timeout=TIMEOUT
        )

        self.assertEqual(
            response.status_code,
            200
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

        self.assertEqual(
            response.status_code,
            200
        )

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

        self.assertEqual(
            response.status_code,
            200
        )
