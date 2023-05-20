from functools import cache

from burrito.utils.auth import get_auth_core
from burrito.utils.db_utils import get_user_by_id

from burrito.utils.permissions_checker import check_permission

from burrito.utils.logger import get_logger

from burrito.models.statuses_model import Statuses
from burrito.models.tickets_model import Tickets
from burrito.schemas.tickets_schema import (
    UpdateTicketSchema
)

from burrito.utils.tickets_util import (
    is_ticket_exist,
    am_i_own_this_ticket,
    am_i_own_this_ticket_with_error
)


__all__ = (
    "get_auth_core",
    "get_user_by_id",
    "check_permission",
    "is_ticket_exist",
    "am_i_own_this_ticket",
    "am_i_own_this_ticket_with_error"
)


def update_ticket_info(
    ticket_object: Tickets,
    data: UpdateTicketSchema
) -> None:
    if data.subject:
        ticket_object.subject = data.subject

    if data.body:
        ticket_object.body = data.body

    if isinstance(data.hidden, bool):
        ticket_object.hidden = data.hidden

    if isinstance(data.anonymous, bool):
        ticket_object.anonymous = data.anonymous

    ticket_object.save()


@cache
def get_status_close_id() -> Statuses:
    status_name = "CLOSE"
    status_object = Statuses.get_or_none(Statuses.name == status_name)

    if not status_object:
        get_logger().critical(f"Status {status_name} is not exist in database")

    return status_object
