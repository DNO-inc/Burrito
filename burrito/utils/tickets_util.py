from typing import Any, Literal

import orjson
from fastapi import HTTPException, status
from playhouse.shortcuts import model_to_dict
from redis import Redis

from burrito.models.bookmarks_model import Bookmarks
from burrito.models.division_model import Divisions
from burrito.models.liked_model import Liked
from burrito.models.m_actions_model import Actions, BaseAction, FileActions
from burrito.models.m_notifications_model import NotificationMetaData, Notifications
from burrito.models.queues_model import Queues
from burrito.models.statuses_model import Statuses
from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users
from burrito.schemas.action_schema import ActionSchema, FileActionSchema
from burrito.schemas.comment_schema import (
    CommentBaseDetailInfoSchema,
    CommentDetailInfoScheme,
)
from burrito.schemas.division_schema import DivisionResponseSchema
from burrito.schemas.tickets_schema import TicketUsersInfoSchema
from burrito.utils.email_templates import (
    TEMPLATE__ASSIGNED_TO_TICKET,
    TEMPLATE__EMAIL_NOTIFICATION,
    TEMPLATE__UNASSIGNED_TO_TICKET,
)
from burrito.utils.email_util import publish_email
from burrito.utils.logger import get_logger
from burrito.utils.mongo_util import (
    mongo_delete,
    mongo_insert,
    mongo_items_count,
    mongo_select,
)
from burrito.utils.query_util import STATUS_ACCEPTED
from burrito.utils.redis_utils import get_redis_connector
from burrito.utils.users_util import get_user_by_id, get_user_by_id_or_none, is_admin
from burrito.utils.websockets import make_websocket_message

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
    """
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
    user_dict_data["division"] = DivisionResponseSchema(
        **model_to_dict(user.division)
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
            TEMPLATE__EMAIL_NOTIFICATION["subject"].format(
                ticket_id=ticket.ticket_id,
                ticket_subject=ticket.subject
            ),
            TEMPLATE__EMAIL_NOTIFICATION["content"].format(
                data=f"{action_author.login} змінив значення '{field_name}' з ({old_value}) на ({new_value})"
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
        New file action (
            ticket={ticket_id},
            user={user_id},
            value={value}
            file_meta_action={file_meta_action}
        )

        """
    )
    action_id = mongo_insert(
        FileActions(
            ticket_id=ticket_id,
            user_id=user_id,
            value=value,
            file_meta_action=file_meta_action
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


def _assemble_action(history_item: dict, ticket: Tickets, current_user_id: int) -> BaseAction:
    """
    Represent action from the mongodb as action's class

    Args:
        history_item: The dict representing the action
        ticket: The ticket object
        current_user_id: user ID for which we are trying to extract history

    Returns:
        FileActionSchema or ActionSchema depending on the type of action
    """
    is_ticket_owner = am_i_own_this_ticket(ticket.creator.user_id, current_user_id)

    if history_item["field_name"] == "file":
        return FileActionSchema(
            ticket_id=history_item["ticket_id"],
            author=make_short_user_data(
                history_item["user_id"],
                hide_user_id=False if is_ticket_owner else (
                    ticket.anonymous and (history_item["user_id"] == ticket.creator.user_id)
                )
            ),
            creation_date=history_item["creation_date"],
            field_name=history_item["field_name"],
            value=history_item["value"],
            file_meta_action=history_item["file_meta_action"]
        )

    old_value = history_item["old_value"]
    new_value = history_item["new_value"]

    if history_item["field_name"] == "assignee":
        old_assignee = get_user_by_id_or_none(history_item["old_value"])
        new_assignee = get_user_by_id_or_none(history_item["new_value"])

        old_value = old_assignee.login if old_assignee else history_item["old_value"]
        new_value = new_assignee.login if new_assignee else history_item["new_value"]

    return ActionSchema(
        ticket_id=history_item["ticket_id"],
        author=make_short_user_data(
            history_item["user_id"],
            hide_user_id=False if is_ticket_owner else (
                ticket.anonymous and (history_item["user_id"] == ticket.creator.user_id)
            )
        ),
        creation_date=history_item["creation_date"],
        field_name=history_item["field_name"],
        old_value=old_value,
        new_value=new_value
    )


def _assemble_comment(history_item: dict, ticket: Tickets, current_user_id: int) -> CommentDetailInfoScheme:
    """
    Represent comment from mongodb as object.

    Args:
        history_item: The dict representing the action (with action type 'comment')
        ticket: The ticket object
        current_user_id: user ID for which we are trying to extract history

    Returns:
        An object representing a comment
    """
    additional_data = mongo_select(Actions, _id=history_item["reply_to"]) if history_item["reply_to"] else None
    # If additional_data is set to true the data is added to the list of additional data.
    if additional_data:
        additional_data = additional_data[0]

    is_ticket_owner = am_i_own_this_ticket(ticket.creator.user_id, current_user_id)

    return CommentDetailInfoScheme(
        reply_to=CommentBaseDetailInfoSchema(
            comment_id=str(additional_data["_id"]),
            author=make_short_user_data(
                additional_data["author_id"],
                hide_user_id=False if is_ticket_owner else (
                    ticket.anonymous and (additional_data["author_id"] == ticket.creator.user_id)
                )
            ),
            body=additional_data["body"],
            creation_date=additional_data["creation_date"]
        ) if additional_data else None,
        comment_id=str(history_item["_id"]),
        author=make_short_user_data(
            history_item["author_id"],
            hide_user_id=False if is_ticket_owner else (
                ticket.anonymous and (history_item["author_id"] == ticket.creator.user_id)
            )
        ),
        body=history_item["body"],
        creation_date=history_item["creation_date"]
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

    result: list[BaseAction | CommentDetailInfoScheme] = []

    for item in mongo_select(Actions, start_page, items_count, "creation_date", True, ticket_id=ticket.ticket_id):
        if item["type_"] == "action":
            result.append(_assemble_action(item, ticket, user_id))

        elif item["type_"] == "comment":
            result.append(_assemble_comment(item, ticket, user_id))

    return result


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
    if ticket.queue is None or ticket.queue.queue_id != new_queue.queue_id:
        create_ticket_action(
            ticket_id=ticket.ticket_id,
            user_id=user_id,
            field_name="queue",
            old_value="None" if ticket.queue is None else (
                f"{ticket.queue.division.name}{__Q_SEP}{ticket.queue.scope}{__Q_SEP}{ticket.queue.name}"
            ),
            new_value=f"{new_queue.division.name}{__Q_SEP}{new_queue.scope}{__Q_SEP}{new_queue.name}"
        )
        ticket.queue = new_queue


def change_ticket_division(ticket: Tickets | int, user_id: int, new_division: Divisions) -> None:
    """
    Change the division of a ticket.

    Args:
        ticket: Ticket to change the division of.
        user_id: User who made the change.
        new_division: New division to set.
    """
    if isinstance(ticket, int):
        ticket = is_ticket_exist(ticket)

    # creates a ticket action if the ticket's division is different than the new one.
    if ticket.division.division_id != new_division.division_id:
        create_ticket_action(
            ticket_id=ticket.ticket_id,
            user_id=user_id,
            field_name="division",
            old_value=ticket.division.name,
            new_value=new_division.name
        )
        ticket.division = new_division


def _assign_new_people(ticket: Tickets, initiator_id: int, new_assignee: Users, email_template_data: dict):
    """
    Assign a new assignee to a ticket and sends email.
    This is a helper function for : meth : ` change_ticket_assignee `.

    Args:
        ticket: The ticket to be updated.
        initiator_id: The ID of the user who initiates
        new_assignee: The new assignee to assign
        email_template_data: Data to be passed to the email
    """
    create_ticket_action(
        ticket_id=ticket.ticket_id,
        user_id=initiator_id,
        field_name="assignee",
        old_value="None",
        new_value=new_assignee.user_id
    )
    ticket.assignee = new_assignee

    change_ticket_status(ticket, initiator_id, STATUS_ACCEPTED)

    publish_email(
        (new_assignee.user_id,),
        TEMPLATE__ASSIGNED_TO_TICKET["subject"].format(**email_template_data),
        TEMPLATE__ASSIGNED_TO_TICKET["content"].format(**email_template_data)
    )


def _reassign_people(ticket: Tickets, initiator_id: int, new_assignee: Users, email_template_data: dict):
    """
    Reassign new people to a ticket and sends email.
    This is a helper function for : meth : ` change_ticket_assignee `.

    Args:
        ticket: The ticket to reassign people to.
        initiator_id: The ID of the user who initiates the ticket.
        new_assignee: The new assignee of the ticket.
        email_template_data: Data to be used in the email
    """
    create_ticket_action(
        ticket_id=ticket.ticket_id,
        user_id=initiator_id,
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


def _remove_assignee(ticket: Tickets, initiator_id: int, email_template_data: dict):
    """
    Removes assignee from ticket and sends email to unassigned user.

    Args:
        ticket: Ticket to remove assignee from
        initiator_id: ID of user who is trying to unassign assignee
        email_template_data: Data to be used in the email
    """
    create_ticket_action(
        ticket_id=ticket.ticket_id,
        user_id=initiator_id,
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


def change_ticket_assignee(ticket: Tickets | int, user_id: int, new_assignee: Users | None) -> None:
    """
    Change assignee of ticket.

    Args:
        ticket: ticket to change assignee of
        user_id: ID of user who is changing assignee
        new_assignee: new assignee of ticket
    """
    if not is_admin(new_assignee):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This user is not admin"
        )

    if isinstance(ticket, int):
        ticket = is_ticket_exist(ticket)

    email_template_data = {
        "ticket_id": ticket.ticket_id,
        "ticket_subject": ticket.subject
    }

    if new_assignee and (not ticket.assignee):
        _assign_new_people(ticket, user_id, new_assignee, email_template_data)

    elif new_assignee and ticket.assignee and ticket.assignee.user_id != new_assignee.user_id:
        _reassign_people(ticket, user_id, new_assignee, email_template_data)

    elif new_assignee is None and ticket.assignee and ticket.assignee.user_id == user_id:
        _remove_assignee(ticket, user_id, email_template_data)


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


def can_i_interact_with_ticket(ticket: Tickets | int, user: Users | int) -> bool:
    """
    Checks if user can interact with ticket.

    Args:
        ticket: ID or Tickets instance to check if it's allowed to interact
        user_id: ID or Users instance who wants to interact with ticket

    Returns:
        True if user can interact with ticket else False
    """

    if isinstance(ticket, int):
        ticket = is_ticket_exist(ticket)

    if isinstance(user, int):
        user = get_user_by_id(user)

    return (
        ticket.hidden == 0
        or user.user_id in (ticket.creator.user_id, ticket.assignee.user_id if ticket.assignee else -1)
        or is_admin(user)
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
