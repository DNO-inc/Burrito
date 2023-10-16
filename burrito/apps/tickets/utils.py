from typing import Any
from functools import cache

from burrito.utils.auth import get_auth_core
from burrito.utils.users_util import get_user_by_id

from burrito.utils.permissions_checker import check_permission

from burrito.utils.logger import get_logger

from burrito.models.bookmarks_model import Bookmarks
from burrito.models.statuses_model import Statuses
from burrito.models.tickets_model import Tickets
from burrito.models.queues_model import Queues
from burrito.models.liked_model import Liked
from burrito.models.user_model import Users

from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
from burrito.schemas.queue_schema import QueueResponseSchema
from burrito.schemas.tickets_schema import (
    UpdateTicketSchema,
    TicketDetailInfoSchema
)

from burrito.utils.auth import AuthTokenPayload
from burrito.utils.tickets_util import (
    is_ticket_exist,
    am_i_own_this_ticket,
    am_i_own_this_ticket_with_error,
    is_ticket_followed,
    is_ticket_bookmarked,
    is_ticket_liked,
    hide_ticket_body
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


def make_ticket_detail_info(
        ticket: Tickets,
        token_payload: AuthTokenPayload,
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
        faculty=FacultyResponseSchema(
            faculty_id=ticket.faculty.faculty_id,
            name=ticket.faculty.name
        ),
        queue=QueueResponseSchema(
            queue_id=queue.queue_id,
            faculty=queue.faculty.faculty_id,
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
        is_liked=is_ticket_liked(token_payload.user_id, ticket.ticket_id),
        is_followed=is_ticket_followed(token_payload.user_id, ticket.ticket_id),
        is_bookmarked=is_ticket_bookmarked(token_payload.user_id, ticket.ticket_id),
        date=str(ticket.created)
    )


def get_filtered_bookmarks(
    _filters: list[Any],
    _desc: bool = True,
    start_page: int = 1,
    tickets_count: int = 10
) -> list[Tickets]:
    if _filters:
        return Tickets.select(
            Tickets
        ).join(
            Bookmarks,
            on=(Tickets.ticket_id == Bookmarks.ticket)
        ).where(*_filters).paginate(
            start_page,
            tickets_count
        ).order_by(
            Bookmarks.created.desc() if _desc else Bookmarks.created
        )

    return Tickets.select(
        Tickets
    ).join(
        Bookmarks,
        on=(Tickets.ticket_id == Bookmarks.ticket)
    ).paginate(
        start_page,
        tickets_count
    ).order_by(
        Bookmarks.created.desc() if _desc else Bookmarks.created
    )


def get_filtered_bookmarks_count(
    _filters: list[Any],
    start_page: int = 1,
    tickets_count: int = 10
) -> int:
    return get_filtered_bookmarks(
        _filters,
        start_page=start_page,
        tickets_count=tickets_count
    ).count()
