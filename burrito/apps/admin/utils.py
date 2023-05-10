from burrito.utils.base_view import BaseView, status
from burrito.utils.permissions_checker import check_permission

from burrito.models.tickets_model import Tickets

__all__ = [
    "BaseView",
    "status",
    "check_permission"
]


def is_ticket_exist(ticket_id: int) -> Tickets | None:
    return Tickets.get_or_none(
        Tickets.ticket_id == ticket_id
    )
