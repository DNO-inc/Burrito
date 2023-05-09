from burrito.utils.auth import get_auth_core
from burrito.utils.db_utils import get_user_by_id

from burrito.utils.base_view import BaseView, status
from burrito.utils.permissions_checker import check_permission

from burrito.models.tickets_model import Tickets
from burrito.schemas.tickets_schema import UpdateTicket


__all__ = (
    "get_auth_core",
    "get_user_by_id",
    "BaseView",
    "status",
    "check_permission"
)


def is_ticket_exist(ticket_id: int) -> Tickets | None:
    return Tickets.get_or_none(
        Tickets.ticket_id == ticket_id
    )


def update_ticket_info(ticket_object: Tickets, data: UpdateTicket) -> None:
    if data.subject:
        ticket_object.subject = data.subject

    if data.body:
        ticket_object.body = data.body

    if isinstance(data.hidden, bool):
        ticket_object.hidden = data.hidden

    if isinstance(data.anonymous, bool):
        ticket_object.anonymous = data.anonymous

    ticket_object.save()
