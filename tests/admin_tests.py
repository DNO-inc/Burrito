import unittest
import requests
import random

from auth_test import AuthTestCase


class AdminTestCase(unittest.TestCase):
    @unittest.skip
    def test_admin_delete_ticket(self):
        response = requests.delete(
            "http://127.0.0.1:8080/admin/tickets/delete",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "ticket_id": 8
            },
            timeout=0.5
        )

        self.assertEqual(
            response.status_code,
            200
        )

    @unittest.skip
    def test_admin_update_ticket(self):
        response = requests.post(
            "http://127.0.0.1:8080/admin/tickets/update",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "ticket_id": 11,
                "status_id": random.randint(1, 6)
            },
            timeout=0.5
        )

        self.assertEqual(
            response.status_code,
            200
        )

    @unittest.skip
    def test_admin_ticket_list_view(self):
        response = requests.post(
            "http://127.0.0.1:8080/admin/tickets/ticket_list",
            headers={
               "Authorization": f"Bearer {AuthTestCase.access_token}"
            },
            json={
                "hidden": True
            },
            timeout=1
        )
        print(response.json())
        self.assertEqual(
            response.status_code,
            200
        )
