from peewee import Expression

from burrito.models.statuses_model import Statuses
from burrito.models.tickets_model import Tickets

from burrito.utils.converter import (
    StatusStrToModel,
    FacultyStrToModel,
    QueueStrToModel
)


_PROTECTED_STATUSES: tuple[int] = (
    StatusStrToModel.convert("NEW").status_id,
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


def q_hidden() -> Expression:
    return Tickets.hidden == 0


def q_protected_statuses() -> Expression:
    return Tickets.status.not_in(_PROTECTED_STATUSES)


def q_is_valid_faculty(value: str) -> Expression:
    return Tickets.faculty == FacultyStrToModel.convert(value)


def q_is_valid_queue(queue: str, faculty: str) -> Expression:
    return Tickets.queue == QueueStrToModel.convert(queue, faculty)


def q_is_valid_status(value: str) -> Expression:
    return Tickets.status == StatusStrToModel.convert(value)


def q_is_valid_status_list(values: list[str]) -> Expression | None:
    if not values:
        return None

    result_query = q_is_valid_status(values[0])

    for item in values[1:]:
        result_query |= q_is_valid_status(item)
    return result_query
