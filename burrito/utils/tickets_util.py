from typing import Any, Literal
import orjson

from redis import Redis
from fastapi import HTTPException, status
from playhouse.shortcuts import model_to_dict

from burrito.utils.logger import get_logger
from burrito.utils.query_util import ADMIN_ROLES, STATUS_ACCEPTED
from burrito.utils.users_util import get_user_by_id, get_user_by_id_or_none
from burrito.utils.mongo_util import mongo_insert, mongo_select, mongo_delete, mongo_items_count
from burrito.utils.redis_utils import get_redis_connector
from burrito.utils.websockets import make_websocket_message
from burrito.utils.email_util import publish_email, EMAIL_NOTIFICATION_TEMPLATE
from burrito.utils.email_templates import (
    TEMPLATE__ASSIGNED_TO_TICKET,
    TEMPLATE__UNASSIGNED_TO_TICKET
)

from burrito.models.statuses_model import Statuses
from burrito.models.queues_model import Queues
from burrito.models.faculty_model import Faculties
from burrito.models.bookmarks_model import Bookmarks
from burrito.models.liked_model import Liked
from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users

from burrito.models.m_actions_model import Actions, FileActions
from burrito.models.m_notifications_model import Notifications, NotificationMetaData

from burrito.schemas.action_schema import ActionSchema, FileActionSchema
from burrito.schemas.tickets_schema import TicketUsersInfoSchema
from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.comment_schema import CommentDetailInfoScheme, CommentBaseDetailInfoSchema


__FILE_NOTIFICATION_LIST = {
    "upload": {
        "en": "{} has uploaded a file {}",
        "ua": "{} завантажив файл {}"
    },
    "delete": {
        "en": "{} has deleted the file {}",
        "ua": "{} видалив файл {}"
    },
}
__Q_SEP = " > "  # separator for queue actions


def is_ticket_exist(ticket_id: int) -> Tickets | None:
    """_summary_

    Args:
        ticket_id (int): ticket ID

    Returns:
        Tickets | None: return ticket object if exist else raise an error
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
    """
    Checks if the user is the creator of the ticket. This is used to ensure that a ticket is owned by user

    Args:
        ticket_creator_id: ID of the user who created the ticket
        user_id: ID of the user who might be creator of the ticket

    Returns: 
        True if the user is the ticket creator else False
    """
    return ticket_creator_id == user_id


def am_i_own_this_ticket_with_error(
    ticket_creator_id: int, user_id: int
) -> bool | None:
    """
    Check if the user is allowed to interact with this ticket.
    This is a wrapper around am_i_own_this_ticket that raises HTTPException in case of permission denied.

    Args:
        ticket_creator_id: ID of the ticket creator
        user_id: ID of the user to check permissions for

    Returns:
        True if the user is allowed to interact with this
    """

    if not am_i_own_this_ticket(ticket_creator_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have not permissions to interact with this ticket"
        )

    return True


def hide_ticket_body(body: str, result_length: int = 500) -> str:
    """
    Hide ticket body. This is used to cut ticket body.
    
    Args:
        body: The body of the ticket.
        result_length: The length of the ticket body that will be returned for user.

    Returns: 
        The ticket body truncated to `result_length` characters
    """
    return body[:result_length] + ("..." if len(body) >= result_length else "")


def make_short_user_data(
    user: Users | int,
    *,
    hide_user_id: bool = True
) -> TicketUsersInfoSchema:
    """
    Make a TicketUsersInfoSchema object that can be used to create a short user.

    Args:
        user: The user whose data need to verify or hide
        hide_user_id: Used if you need to hide user data, for example when ticket is anonymous.

    Returns:
        An object that describes user
    """

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
    """
    Checks if a user is following a ticket.

    Args:
        user_id: ID of the user to check.
        ticket_id: ID of the ticket to check.

    Returns:
        True if the user is following the ticket False otherwise
    """
    return bool(
        Tickets.select(Tickets.ticket_id).join(
            Bookmarks,
            on=(Tickets.ticket_id == Bookmarks.ticket)
        ).where(
            Bookmarks.user == user_id,
            Tickets.creator != user_id,
            Tickets.ticket_id == ticket_id
        ).get_or_none()
    )


def is_ticket_bookmarked(user_id: int, ticket_id: int) -> bool:
    """
    Check if a ticket is bookmarked by a user.

    Args:
        user_id: ID of the user to check
        ticket_id: ID of the ticket to check if it is bookmarked

    Returns:
        True if the ticket is bookmarked else False
    """
    return bool(
        Tickets.select(Tickets.ticket_id).join(
            Bookmarks,
            on=(Tickets.ticket_id == Bookmarks.ticket)
        ).where(
            Bookmarks.user == user_id,
            Tickets.creator == user_id,
            Tickets.ticket_id == ticket_id
        ).get_or_none()
    )


def is_ticket_liked(user_id: int, ticket_id: int) -> bool:
    """
    Check if a user likes a ticket. This is used to prevent spamming the user's ticket when they're in the middle of a ticket.

    Args:
        user_id: ID of the user. It's the user ID
        ticket_id: ID of the ticket. It's the ticket ID

    Returns:
        True if the user likes the ticket False otherwise
    """
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
    """
    Select filters to apply to a role.

    Args:
        role_name: The name of the role.
        filter_package: The package of filters.

    Returns:
        A list of filter names that should be applied when selecting tickets
    """

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
    """
    Get tickets filtered by given filters.

    Args:
        _filters: a list of filters to apply to the query
        _desc: whether to sort the results in descending or ascending
        start_page: the page to start with
        tickets_count: the number of tickets to return

    Returns:
        a list of tickets ordered by creation date
    """

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
    """
    Create a new action. This will be used when something changed in a ticket

    Args:
        ticket_id: The ID of the ticket
        user_id: The ID of the user who made the change
        field_name: The name of the field that was changed
        old_value: The old value of the field that was changed
        new_value: The new value of the field that was changed
        generate_notification: Whether or not to generate notifications for the change
    """

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
    action_id = mongo_insert(
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
                field_name={field_name},
                old_value={old_value},
                new_value={new_value}
            )

            """
        )

        ticket: Tickets = is_ticket_exist(ticket_id)

        action_author: Users = get_user_by_id(user_id)

        if field_name == "assignee":
            old_assignee = get_user_by_id_or_none(old_value)
            new_assignee = get_user_by_id_or_none(new_value)

            old_value = old_assignee.login if old_assignee else old_value
            new_value = new_assignee.login if new_assignee else new_value

        send_notification(
            ticket,
            Notifications(
                ticket_id=ticket_id,
                user_id=user_id,
                body_ua=f"{action_author.login} змінив значення '{field_name}' з ({old_value}) на ({new_value})",
                body=f"{action_author.login} changed the value '{field_name}' from ({old_value}) to ({new_value})"
            ),
            author_id=user_id
        )
        publish_email(
            get_notification_receivers(ticket, exclude_id=user_id),
            f"TreS #{ticket.ticket_id} \"{ticket.subject}\"",
            EMAIL_NOTIFICATION_TEMPLATE.format(
                f"{action_author.login} змінив значення '{field_name}' з ({old_value}) на ({new_value})"
            )
        )
        get_redis_connector().publish(
            f"chat_{ticket_id}",
            orjson.dumps(
                {
                    "action_id": action_id,
                    "msg_type": "MSG_ACTION"
                }
            )
        )


def create_ticket_file_action(
    *,
    ticket_id: int,
    user_id: int,
    value: str,
    file_meta_action: Literal["upload", "delete"],
    generate_notification: bool = True
) -> None:
    """
    Create file action and notify about it.

    Args:
        ticket_id: ID of the ticket
        user_id: ID of the user who made the change
        value: file name
        file_meta_action: determine what happened with file (uploaded or deleted)
        generate_notification: flag to generate notification
    """

    get_logger().info(
        f"""
        New fila action (
            ticket={ticket_id},
            user={user_id},
            value={value}
        )

        """
    )
    action_id = mongo_insert(
        FileActions(
            ticket_id=ticket_id,
            user_id=user_id,
            value=value
        )
    )
    if generate_notification:
        get_logger().info(
            f"""
            New notification (
                ticket={ticket_id},
                user={user_id},
                body={value}
            )

            """
        )

        ticket: Tickets = is_ticket_exist(ticket_id)
        action_author: Users = get_user_by_id(user_id)

        notification_text = __FILE_NOTIFICATION_LIST[file_meta_action]
        send_notification(
            ticket,
            Notifications(
                ticket_id=ticket_id,
                user_id=user_id,
                body_ua=notification_text["ua"].format(action_author.login, value),
                body=notification_text["en"].format(action_author.login, value)
            ),
            author_id=user_id
        )
        get_redis_connector().publish(
            f"chat_{ticket_id}",
            orjson.dumps(
                {
                    "action_id": action_id,
                    "msg_type": "MSG_FILE_ACTION"
                }
            )
        )


def get_ticket_history(ticket: Tickets | int, user_id: int, start_page: int = 1, items_count: int = 10) -> list[object]:
    """
    Get ticket history. This function is used to get a list of actions that have been created by user.

    Args:
        ticket: Ticket to get history for.
        user_id: ID of the user who requested ticket history.
        start_page: Page number to start from.
        items_count: Number of items to get.

    Returns:
        List of actions
    """
    if isinstance(ticket, int):
        ticket = is_ticket_exist(ticket)

    ticket_owner = am_i_own_this_ticket(ticket.creator.user_id, user_id)

    result = []

    for item in mongo_select(Actions, start_page, items_count, "creation_date", True, ticket_id=ticket.ticket_id):
        if item["type_"] == "action":
            if item["field_name"] == "file":
                result.append(
                    FileActionSchema(
                        ticket_id=item["ticket_id"],
                        author=make_short_user_data(
                            item["user_id"],
                            hide_user_id=False if ticket_owner else (ticket.anonymous and (item["user_id"] == ticket.creator.user_id))
                        ),
                        creation_date=item["creation_date"],
                        field_name=item["field_name"],
                        value=item["value"]
                    )
                )

            else:
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
    """
    Checks if user can interact with ticket.

    Args:
        ticket: Ticket to check if allowed to interact `user_id`
        user_id: ID of user who wants to interact with ticket

    Returns:
        True if user can interact with ticket else False
    """
    if isinstance(ticket, int):
        ticket = is_ticket_exist(ticket)

    return (
        (ticket.creator.user_id == user_id)
        or user_id in [admin.user_id for admin in Users.select().where(Users.role.in_(ADMIN_ROLES))]
        or ticket.hidden == 0
    )


def change_ticket_status(ticket: Tickets | int, user_id: int, new_status: Statuses) -> None:
    """
    Change ticket status. This function is used to change status of ticket.
    The ticket will not changed if previous status the same as new.

    Args:
        ticket: Ticket to change status of.
        user_id: User who made the change.
        new_status: New status of ticket.
    """
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
    """
    Change the queue of a ticket.

    Args:
        ticket: Ticket to change queue of
        user_id: User who made the change.
        new_queue: New queue to change

    Returns:
        None on success Exception on failure Raises an exception on
    """
    if isinstance(ticket, int):
        ticket = is_ticket_exist(ticket)

    # Set the queue if not already set.
    if ticket.queue is None:
        create_ticket_action(
            ticket_id=ticket.ticket_id,
            user_id=user_id,
            field_name="queue",
            old_value="None",
            new_value=f"{new_queue.faculty.name}{__Q_SEP}{new_queue.scope}{__Q_SEP}{new_queue.name}"
        )
        ticket.queue = new_queue

    elif ticket.queue.queue_id != new_queue.queue_id:
        create_ticket_action(
            ticket_id=ticket.ticket_id,
            user_id=user_id,
            field_name="queue",
            old_value=f"{ticket.queue.faculty.name}{__Q_SEP}{ticket.queue.scope}{__Q_SEP}{ticket.queue.name}",
            new_value=f"{new_queue.faculty.name}{__Q_SEP}{new_queue.scope}{__Q_SEP}{new_queue.name}"
        )
        ticket.queue = new_queue


def change_ticket_faculty(ticket: Tickets | int, user_id: int, new_faculty: Faculties) -> None:
    """
    Change the faculty of a ticket.

    Args:
        ticket: Ticket to change the faculty of.
        user_id: User who made the change.
        new_faculty: New faculty to set.
    """
    if isinstance(ticket, int):
        ticket = is_ticket_exist(ticket)

    # creates a ticket action if the ticket's faculty is different than the new one.
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
    """
    Change assignee of ticket.

    Args:
        ticket: ticket to change assignee of
        user_id: ID of user who is changing assignee
        new_assignee: new assignee of ticket
    """
    if isinstance(ticket, int):
        ticket = is_ticket_exist(ticket)

    email_template_data = {
        "ticket_id": ticket.ticket_id,
        "ticket_subject": ticket.subject
    }

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

        publish_email(
            (new_assignee.user_id,),
            TEMPLATE__ASSIGNED_TO_TICKET["subject"].format(**email_template_data),
            TEMPLATE__ASSIGNED_TO_TICKET["content"].format(**email_template_data)
        )

    elif new_assignee and ticket.assignee and ticket.assignee.user_id != new_assignee.user_id:
        create_ticket_action(
            ticket_id=ticket.ticket_id,
            user_id=user_id,
            field_name="assignee",
            old_value=ticket.assignee.user_id,
            new_value=new_assignee.user_id
        )
        publish_email(
            (ticket.assignee.user_id,),
            TEMPLATE__UNASSIGNED_TO_TICKET["subject"].format(**email_template_data),
            TEMPLATE__UNASSIGNED_TO_TICKET["content"].format(**email_template_data)
        )
        publish_email(
            (new_assignee.user_id,),
            TEMPLATE__ASSIGNED_TO_TICKET["subject"].format(**email_template_data),
            TEMPLATE__ASSIGNED_TO_TICKET["content"].format(**email_template_data)
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

        publish_email(
            (ticket.assignee.user_id,),
            TEMPLATE__UNASSIGNED_TO_TICKET["subject"].format(**email_template_data),
            TEMPLATE__UNASSIGNED_TO_TICKET["content"].format(**email_template_data)
        )

        ticket.assignee = None


def get_notification_receivers(ticket: Tickets | int, exclude_id: int | None = None) -> set[int]:
    """
    Get notification receivers for ticket.
    This is used to determine who should receive notification

    Creator, assignee and users who followed this ticket can receive notifications related to `ticket`

    Args:
        ticket: ticket ID

    Returns:
        Set of user_ids who receive notification's
    """
    if isinstance(ticket, int):
        ticket = is_ticket_exist(ticket)

    # TODO: change this solution
    ids = {item.user.user_id for item in Bookmarks.select(Bookmarks.user).where(Bookmarks.ticket == ticket.ticket_id)}
    ids.add(ticket.creator.user_id)
    if ticket.assignee:
        ids.add(ticket.assignee.user_id)

    if exclude_id and exclude_id in ids:
        ids.remove(exclude_id)

    return ids


def send_notification(ticket: Tickets | int, notification: Notifications, author_id: int):
    """
    Send notification to subscribers.

    Args:
        ticket: ticket ID or ticket object
        notification: notification to be sent to subscribers
    """
    if isinstance(ticket, int):
        ticket = is_ticket_exist(ticket)

    pubsub: Redis = get_redis_connector()

    target_ids = get_notification_receivers(ticket, exclude_id=author_id)
    notification_id = mongo_insert(notification)

    try:
        for id_ in target_ids:
            # save notification meta data in case if user is offline
            # when user became online he can received notifications via `/notifications/` endpoint
            meta_data_id = mongo_insert(
                NotificationMetaData(
                    user_id=id_,
                    notification_id=notification_id
                )
            )
            # Publishes a notification to users chanel
            subscribers_count = pubsub.publish(
                f"user_{id_}",
                make_websocket_message(
                    type_="notification",
                    obj=notification
                )
            )

            # Delete the notification meta data if user is online and received notification via websocket connection
            if subscribers_count > 0:
                mongo_delete(NotificationMetaData, _id=meta_data_id)

        # Delete notifications from the database if all users was online and received notification via websocket connection
        if mongo_items_count(NotificationMetaData, notification_id=notification_id) == 0:
            mongo_delete(Notifications, _id=notification_id)

    except Exception:
        get_logger().error(
            f"""
                target_ids: {target_ids}
            """
        )


def send_comment_update(ticket_id: int, comment_id: str, msg_type: Literal["MSG_CREATE", "MSG_EDIT", "MSG_DELETE"]) -> None:
    """
    Sends a comment update to the chat (Redis pub/sub chanel).
    Than that data will be used by websocket data

    Args:
        ticket_id: The ID of the ticket
        comment_id: The ID of the comment
    """
    get_redis_connector().publish(
        f"chat_{ticket_id}",
        orjson.dumps(
            {
                "comment_id": comment_id,
                "msg_type": msg_type
            }
        )
    )
