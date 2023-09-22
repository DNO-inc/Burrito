from typing import Any

from redis import Redis
from fastapi import HTTPException, status
from playhouse.shortcuts import model_to_dict

from burrito.utils.logger import get_logger
from burrito.utils.query_util import ADMIN_ROLES, STATUS_ACCEPTED
from burrito.utils.users_util import get_user_by_id, get_user_by_id_or_none
from burrito.utils.mongo_util import mongo_insert, mongo_select
from burrito.utils.redis_utils import get_redis_connector
from burrito.utils.websockets import make_websocket_message

from burrito.models.statuses_model import Statuses
from burrito.models.queues_model import Queues
from burrito.models.faculty_model import Faculties
from burrito.models.bookmarks_model import Bookmarks
from burrito.models.liked_model import Liked
from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users

from burrito.models.m_actions_model import Actions
from burrito.models.m_notifications_model import Notifications

from burrito.schemas.action_schema import ActionSchema
from burrito.schemas.tickets_schema import TicketUsersInfoSchema
from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.comment_schema import (
    CommentBaseDetailInfoSchema,
    CommentDetailInfoScheme
)


def is_ticket_exist(ticket_id: int) -> Tickets | None:
    """_summary_

    Args:
        ticket_id (int): ticket ID

    Returns:
        Tickets | None: return ticket object if exist else return None
    """

    _ticket = Tickets.get_or_none(
        Tickets.ticket_id == ticket_id
    )

    if not _ticket:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"ticket_id {ticket_id} is not exist"
        )

    return _ticket


def am_i_own_this_ticket(ticket_creator_id: int, user_id: int) -> bool:
    return ticket_creator_id == user_id


def am_i_own_this_ticket_with_error(
    ticket_creator_id: int, user_id: int
) -> bool | None:
    if not am_i_own_this_ticket(ticket_creator_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have not permissions to interact with this ticket"
        )

    return True


def hide_ticket_body(body: str, result_length: int = 500) -> str:
    return body[:result_length] + ("..." if len(body) >= result_length else "")


def make_short_user_data(
    user: Users | int,
    *,
    hide_user_id: bool = True
) -> TicketUsersInfoSchema:
    if isinstance(user, int):
        user = get_user_by_id(user)

    user_dict_data = model_to_dict(user)
    user_dict_data["faculty"] = FacultyResponseSchema(
        **model_to_dict(user.faculty)
    )

    if hide_user_id:
        user_dict_data["user_id"] = None
        user_dict_data["group"] = None
        user_dict_data["firstname"] = None
        user_dict_data["lastname"] = None
        user_dict_data["login"] = None

    return TicketUsersInfoSchema(**user_dict_data)


def is_ticket_followed(user_id: int, ticket_id: int) -> bool:
    return bool(
        Tickets.select(Tickets.ticket_id).join(
            Bookmarks,
            on=(Tickets.ticket_id == Bookmarks.ticket_id)
        ).where(
            Bookmarks.user_id == user_id,
            Tickets.creator != user_id,
            Tickets.ticket_id == ticket_id
        ).get_or_none()
    )


def is_ticket_bookmarked(user_id: int, ticket_id: int) -> bool:
    return bool(
        Tickets.select(Tickets.ticket_id).join(
            Bookmarks,
            on=(Tickets.ticket_id == Bookmarks.ticket_id)
        ).where(
            Bookmarks.user_id == user_id,
            Tickets.creator == user_id,
            Tickets.ticket_id == ticket_id
        ).get_or_none()
    )


def is_ticket_liked(user_id: int, ticket_id: int) -> bool:
    return bool(
        Liked.get_or_none(
            Liked.user_id == user_id,
            Liked.ticket_id == ticket_id
        )
    )


def select_filters(
    role_name: str,
    filter_package: dict[str, dict[str, object]],
) -> list[object]:
    filter_list = filter_package.get(role_name)
    if not filter_list:
        filter_list = filter_package.get("default")

    return [value for value in filter_list if value]


def get_filtered_tickets(
    _filters: list[Any],
    _desc: bool = True,
    start_page: int = 1,
    tickets_count: int = 10
) -> list[Tickets]:
    if _filters:
        return Tickets.select().where(*_filters).paginate(
            start_page,
            tickets_count
        ).order_by(
            Tickets.created.desc() if _desc else Tickets.created
        )

    return Tickets.select().paginate(
        start_page,
        tickets_count
    ).order_by(
        Tickets.created.desc() if _desc else Tickets.created
    )


def create_ticket_action(
    *,
    ticket_id: int,
    user_id: int,
    field_name: str,
    old_value: str,
    new_value: str,
    generate_notification: bool = True
) -> None:
    get_logger().info(
        f"""
        New action (
            ticket={ticket_id},
            user={user_id},
            field_name={field_name},
            old_value={old_value},
            new_value={new_value}
        )

        """
    )
    mongo_insert(
        Actions(
            ticket_id=ticket_id,
            user_id=user_id,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value
        )
    )
    if generate_notification:
        get_logger().info(
            f"""
            New notification (
                ticket={ticket_id},
                user={user_id},
                body={new_value}
            )

            """
        )

        ticket: Tickets = is_ticket_exist(ticket_id)

        ids = [item.user_id for item in Bookmarks.select().where(Bookmarks.ticket_id == ticket_id)]
        ids += [ticket.creator.user_id]
        ids += ([ticket.assignee.user_id] if ticket.assignee else [])
        ids = set(ids)

        pubsub: Redis = get_redis_connector()
        action_author: Users = get_user_by_id(user_id)

        if field_name == "assignee":
            old_assignee = get_user_by_id_or_none(old_value)
            new_assignee = get_user_by_id_or_none(new_value)

            old_value = old_assignee.login if old_assignee else old_value
            new_value = new_assignee.login if new_assignee else new_value

        for id_ in ids:
            pubsub.publish(
                f"user_{id_}",
                make_websocket_message(
                    type_="notification",
                    obj=Notifications(
                        ticket_id=ticket_id,
                        user_id=user_id,
                        body_ua=f"{action_author.login} змінив значення '{field_name}' з ({old_value}) на ({new_value})",
                        body=f"{action_author.login} changed the value '{field_name}' from ({old_value}) to ({new_value})"
                    )
                )
            )


def get_ticket_history(ticket: Tickets | int, user_id: int, start_page: int = 1, items_count: int = 10):
    if isinstance(ticket, int):
        ticket = is_ticket_exist(ticket)

    ticket_owner = am_i_own_this_ticket(ticket.creator.user_id, user_id)

    result = []

    for item in mongo_select(Actions, start_page, items_count, "creation_date", True, ticket_id=ticket.ticket_id):
        if item["type_"] == "action":
            old_value = item["old_value"]
            new_value = item["new_value"]

            if item["field_name"] == "assignee":
                old_assignee = get_user_by_id_or_none(item["old_value"])
                new_assignee = get_user_by_id_or_none(item["new_value"])

                old_value = old_assignee.login if old_assignee else item["old_value"]
                new_value = new_assignee.login if new_assignee else item["new_value"]

            result.append(
                ActionSchema(
                    ticket_id=item["ticket_id"],
                    author=make_short_user_data(
                        item["user_id"],
                        hide_user_id=False if ticket_owner else (ticket.anonymous and (item["user_id"] == ticket.creator.user_id))
                    ),
                    creation_date=item["creation_date"],
                    field_name=item["field_name"],
                    old_value=old_value,
                    new_value=new_value
                )
            )
        elif item["type_"] == "comment":
            additional_data = mongo_select(Actions, _id=item["reply_to"]) if item["reply_to"] else None
            if additional_data:
                additional_data = additional_data[0]

            result.append(
                CommentDetailInfoScheme(
                    reply_to=CommentBaseDetailInfoSchema(
                        comment_id=str(additional_data["_id"]),
                        author=make_short_user_data(
                            additional_data["author_id"],
                            hide_user_id=False if ticket_owner else (ticket.anonymous and (additional_data["author_id"] == ticket.creator.user_id))
                        ),
                        body=additional_data["body"],
                        creation_date=additional_data["creation_date"]
                    ) if additional_data else None,
                    comment_id=str(item["_id"]),
                    author=make_short_user_data(
                        item["author_id"],
                        hide_user_id=False if ticket_owner else (ticket.anonymous and (item["author_id"] == ticket.creator.user_id))
                    ),
                    body=item["body"],
                    creation_date=item["creation_date"]
                )
            )

    return result


def is_allowed_to_interact_with_history(ticket: Tickets | int, user_id: int):
    if isinstance(ticket, int):
        ticket = is_ticket_exist(ticket)

    return (
        (ticket.creator.user_id == user_id)
        or user_id in [admin.user_id for admin in Users.select().where(Users.role.in_(ADMIN_ROLES))]
        or ticket.hidden == 0
    )


def change_ticket_status(ticket: Tickets | int, user_id: int, new_status: Statuses) -> None:
    if isinstance(ticket, int):
        ticket = is_ticket_exist(ticket)

    if ticket.status.status_id != new_status.status_id:
        create_ticket_action(
            ticket_id=ticket.ticket_id,
            user_id=user_id,
            field_name="status",
            old_value=ticket.status.name,
            new_value=new_status.name
        )
        ticket.status = new_status


def change_ticket_queue(ticket: Tickets | int, user_id: int, new_queue: Queues) -> None:
    if isinstance(ticket, int):
        ticket = is_ticket_exist(ticket)

    if ticket.queue is None:
        create_ticket_action(
            ticket_id=ticket.ticket_id,
            user_id=user_id,
            field_name="queue",
            old_value="None",
            new_value=f"{new_queue.faculty.name}/{new_queue.scope}/{new_queue.name}"
        )
        ticket.queue = new_queue

    elif ticket.queue.queue_id != new_queue.queue_id:
        create_ticket_action(
            ticket_id=ticket.ticket_id,
            user_id=user_id,
            field_name="queue",
            old_value=f"{ticket.queue.faculty.name}/{ticket.queue.scope}/{ticket.queue.name}",
            new_value=f"{new_queue.faculty.name}/{new_queue.scope}/{new_queue.name}"
        )
        ticket.queue = new_queue


def change_ticket_faculty(ticket: Tickets | int, user_id: int, new_faculty: Faculties) -> None:
    if isinstance(ticket, int):
        ticket = is_ticket_exist(ticket)

    if ticket.faculty.faculty_id != new_faculty.faculty_id:
        create_ticket_action(
            ticket_id=ticket.ticket_id,
            user_id=user_id,
            field_name="faculty",
            old_value=ticket.faculty.name,
            new_value=new_faculty.name
        )
        ticket.faculty = new_faculty


def change_ticket_assignee(ticket: Tickets | int, user_id: int, new_assignee: Users | None) -> None:
    if isinstance(ticket, int):
        ticket = is_ticket_exist(ticket)

    if new_assignee and (not ticket.assignee):
        create_ticket_action(
            ticket_id=ticket.ticket_id,
            user_id=user_id,
            field_name="assignee",
            old_value="None",
            new_value=new_assignee.user_id
        )
        ticket.assignee = new_assignee

        change_ticket_status(ticket, user_id, STATUS_ACCEPTED)

    elif new_assignee and ticket.assignee.user_id == user_id and ticket.assignee.user_id != new_assignee.user_id:
        create_ticket_action(
            ticket_id=ticket.ticket_id,
            user_id=user_id,
            field_name="assignee",
            old_value=ticket.assignee.user_id,
            new_value=new_assignee.user_id
        )
        ticket.assignee = new_assignee

    elif new_assignee is None and ticket.assignee and ticket.assignee.user_id == user_id:
        create_ticket_action(
            ticket_id=ticket.ticket_id,
            user_id=user_id,
            field_name="assignee",
            old_value=ticket.assignee.user_id,
            new_value="None"
        )
        ticket.assignee = None
