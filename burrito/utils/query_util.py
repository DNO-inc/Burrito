from peewee import Expression

from burrito.models.statuses_model import Statuses
from burrito.models.tickets_model import Tickets
from burrito.models.deleted_model import Deleted

from burrito.utils.converter import (
    StatusConverter,
    FacultyConverter,
    QueueConverter
)


_PROTECTED_STATUSES: tuple[int] = (
    StatusConverter.convert(1).status_id,
)

STATUSES_FOR_USER: list[int] = []
STATUSES_FOR_ADMIN: list[int] = []

for i in Statuses.select():
    if i.status_id not in _PROTECTED_STATUSES:
        STATUSES_FOR_USER.append(i.status_id)
    STATUSES_FOR_ADMIN.append(i.status_id)


def q_is_creator(value) -> Expression:
    if not value:
        return None

    return Tickets.creator == value


def q_is_anonymous(value: bool | int) -> Expression:
    return Tickets.anonymous == value


def q_is_hidden(value: bool | int) -> Expression:
    return Tickets.hidden == value


def q_not_hidden() -> Expression:
    return Tickets.hidden == 0


def q_protected_statuses() -> Expression:
    return Tickets.status.not_in(_PROTECTED_STATUSES)


def q_is_valid_faculty(value: int) -> Expression:
    return Tickets.faculty == FacultyConverter.convert(value)


def q_is_valid_queue(queue: int) -> Expression:
    return Tickets.queue == QueueConverter.convert(queue)


def q_is_valid_status(value: int) -> Expression:
    return Tickets.status == value


def q_is_valid_status_list(values: list[str]) -> Expression | None:
    if not values:
        return None

    result_query = q_is_valid_status(values[0])

    for item in values[1:]:
        result_query |= q_is_valid_status(item)
    return result_query


def q_deleted(_user_id: int) -> Expression:
    return Tickets.ticket_id.in_(
        Deleted.select(Deleted.ticket_id).where(Deleted.user_id == _user_id)
    )


def q_not_deleted(_user_id: int) -> Expression:
    return Tickets.ticket_id.not_in(
        Deleted.select(Deleted.ticket_id).where(Deleted.user_id == _user_id)
    )
