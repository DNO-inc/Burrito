from peewee import Expression

from burrito.models.bookmarks_model import Bookmarks
from burrito.models.statuses_model import Statuses
from burrito.models.tickets_model import Tickets
from burrito.models.deleted_model import Deleted
from burrito.models.queues_model import Queues
from burrito.models.liked_model import Liked

from burrito.utils.converter import (
    StatusConverter,
    FacultyConverter,
)


_PROTECTED_STATUSES: tuple[int] = (1,)

ADMIN_ROLES: list[int] = (9, 10)

STATUS_NEW = StatusConverter.convert(1)
STATUS_ACCEPTED = StatusConverter.convert(2)
STATUS_OPEN = StatusConverter.convert(3)
STATUS_WAITING = StatusConverter.convert(4)
STATUS_REJECTED = StatusConverter.convert(5)
STATUS_CLOSE = StatusConverter.convert(6)
STATUSES_FOR_USER: list[int] = [i.status_id for i in Statuses.select() if i.status_id not in _PROTECTED_STATUSES]
STATUSES_FOR_ADMIN: list[int] = [i.status_id for i in Statuses.select()]


def q_creator_is(value) -> Expression:
    if value is None:
        return None

    return Tickets.creator == value


def q_assignee_is(value) -> Expression:
    if value is None:
        return None

    if value == -1:
        return Tickets.assignee.is_null()

    return Tickets.assignee == value


def q_is_anonymous(value: bool | int) -> Expression:
    if value is None:
        return None

    return Tickets.anonymous == value


def q_is_hidden(value: bool | int) -> Expression:
    if value is None:
        return None

    return Tickets.hidden == value


def q_owned_or_not_hidden(_user_id: int, _hidden: bool) -> Expression:
    if _user_id is None:
        return None

    if _hidden is None:
        return (
            ((Tickets.creator == _user_id) & (q_not_deleted(_user_id)))
            | (q_not_hidden() & q_protected_statuses())
        )
    return (
        ((Tickets.creator == _user_id) & (Tickets.hidden == _hidden) & (q_not_deleted(_user_id)))
        | (q_not_hidden() & q_protected_statuses())
    )


def q_not_hidden() -> Expression:
    return Tickets.hidden == 0


def q_protected_statuses() -> Expression:
    return Tickets.status.not_in(_PROTECTED_STATUSES)


def q_is_valid_faculty(value: int) -> Expression:
    if value is None:
        return None

    return Tickets.faculty == FacultyConverter.convert(value)


def q_scope_is(scope: str) -> Expression:
    if scope is None:
        return None

    return Tickets.queue.in_(
        Queues.select(Queues.queue_id).where(Queues.scope == scope)
    )


def q_is_valid_queue(queues: list[int]) -> Expression:
    if not queues:
        return None

    if -1 in queues:
        new_list = list(filter(lambda x: x >= 0, queues))

        if new_list:
            return Tickets.queue.in_(new_list) | Tickets.queue.is_null()
        return Tickets.queue.is_null()

    return Tickets.queue.in_(queues)


def q_is_valid_status(value: int) -> Expression:
    if value is None:
        return None

    return Tickets.status == StatusConverter.convert(value)


def q_is_valid_status_list(values: list[str]) -> Expression | None:
    if values is None:
        return None

    if not values:
        return None

    result_query = q_is_valid_status(values[0])

    for item in values[1:]:
        result_query |= q_is_valid_status(item)
    return result_query


def q_deleted(_user_id: int) -> Expression:
    if _user_id is None:
        return None

    return Tickets.ticket_id.in_(Deleted.select(Deleted.ticket_id).where(Deleted.user_id == _user_id))


def q_not_deleted(_user_id: int) -> Expression:
    if _user_id is None:
        return None

    return Tickets.ticket_id.not_in(Deleted.select(Deleted.ticket_id).where(Deleted.user_id == _user_id))


def q_bookmarked(_user_id: int) -> Expression:
    if _user_id is None:
        return None

    return Tickets.ticket_id.in_(
        Tickets.select(
            Tickets.ticket_id
        ).join(
            Bookmarks,
            on=(Tickets.ticket_id == Bookmarks.ticket_id)
        ).where(
            Bookmarks.user_id == _user_id,
            Tickets.creator == _user_id
        ).order_by(
            Bookmarks.created.desc()
        )
    )


def q_followed(_user_id: int) -> Expression:
    if _user_id is None:
        return None

    return Tickets.ticket_id.in_(
        Tickets.select(
            Tickets.ticket_id
        ).join(
            Bookmarks,
            on=(Tickets.ticket_id == Bookmarks.ticket_id)
        ).where(
            Bookmarks.user_id == _user_id,
            Tickets.creator != _user_id
        ).order_by(
            Bookmarks.created.desc()
        )
    )


def q_liked(_user_id: int) -> Expression:
    if _user_id is None:
        return None

    return Tickets.ticket_id.in_(Liked.select(Liked.ticket_id).where(Liked.user_id == _user_id))
