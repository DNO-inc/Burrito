import random

import unittest
import requests

from auth_test import AuthTestCase
from tickets_test import TicketsTestCase

TIMEOUT = 5


class AdminTestCase(unittest.TestCase):
    def test_001_admin_update_ticket(self):
        response = requests.post(
            "http://127.0.0.1:8080/admin/tickets/update",
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
            "http://127.0.0.1:8080/admin/tickets/ticket_list",
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
            "http://127.0.0.1:8080/admin/tickets/show",
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
            "http://127.0.0.1:8080/admin/tickets/delete",
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
