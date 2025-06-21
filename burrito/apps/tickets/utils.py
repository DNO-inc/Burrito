from functools import cache

from burrito.models.liked_model import Liked
from burrito.models.queues_model import Queues
from burrito.models.statuses_model import Statuses
from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users
from burrito.schemas.division_schema import DivisionResponseSchema
from burrito.schemas.queue_schema import QueueResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
from burrito.schemas.tickets_schema import TicketDetailInfoSchema, UpdateTicketSchema
from burrito.utils.logger import get_logger
from burrito.utils.permissions_checker import check_permission
from burrito.utils.tickets_util import (
    am_i_own_this_ticket,
    am_i_own_this_ticket_with_error,
    hide_ticket_body,
    is_ticket_bookmarked,
    is_ticket_exist,
    is_ticket_followed,
    is_ticket_liked,
)
from burrito.utils.users_util import get_user_by_id

__all__ = (
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


def make_ticket_detail_info(
        ticket: Tickets,
        current_user: Users,
        creator: Users | None,
        assignee: Users | None,
        *,
        crop_body: bool = True
) -> TicketDetailInfoSchema:

    queue: Queues | None = None
    if ticket.queue:
        queue = Queues.get_or_none(Queues.queue_id == ticket.queue)

    return TicketDetailInfoSchema(
        creator=creator,
        assignee=assignee,
        ticket_id=ticket.ticket_id,
        subject=ticket.subject,
        body=hide_ticket_body(ticket.body, 500) if crop_body else ticket.body,
        hidden=ticket.hidden,
        anonymous=ticket.anonymous,
        division=DivisionResponseSchema(
            division_id=ticket.division.division_id,
            name=ticket.division.name
        ),
        queue=QueueResponseSchema(
            queue_id=queue.queue_id,
            division_id=queue.division.division_id,
            name=queue.name,
            scope=queue.scope
        ) if queue else None,
        status=StatusResponseSchema(
            status_id=ticket.status.status_id,
            name=ticket.status.name,
        ),
        upvotes=Liked.select().where(
            Liked.ticket_id == ticket.ticket_id
        ).count(),
        is_liked=is_ticket_liked(current_user.user_id, ticket.ticket_id),
        is_followed=is_ticket_followed(current_user.user_id, ticket.ticket_id),
        is_bookmarked=is_ticket_bookmarked(current_user.user_id, ticket.ticket_id),
        date=str(ticket.created)
    )
