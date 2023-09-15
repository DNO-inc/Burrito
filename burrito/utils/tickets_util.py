from typing import Any

from fastapi import HTTPException, status

from playhouse.shortcuts import model_to_dict

from burrito.utils.logger import get_logger
from burrito.utils.mongo_util import get_mongo_cursor

from burrito.models.bookmarks_model import Bookmarks
from burrito.models.liked_model import Liked
from burrito.models.tickets_model import Tickets
from burrito.models.actions_model import Actions
from burrito.models.user_model import Users
from burrito.models.comments_model import Comments

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
    user: Users,
    *,
    hide_user_id: bool = True
) -> TicketUsersInfoSchema:
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
    Actions.create(
        ticket=ticket_id,
        user=user_id,
        field_name=field_name,
        old_value=old_value,
        new_value=new_value
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

        get_mongo_cursor()["burrito"]["notifications"].insert_one(
            {
                "ticket_id": ticket_id,
                "user_id": user_id,
                "body": f"{user_id} changed the value '{field_name}' from ({old_value}) to ({new_value})"
            }
        )


def get_ticket_actions(ticket: Tickets) -> list[Actions]:
    return [
        ActionSchema(
            action_id=action.action_id,
            ticket_id=action.ticket_id,
            author=make_short_user_data(
                action.user,
                hide_user_id=(ticket.anonymous and (action.user.user_id == ticket.creator.user_id))
            ),
            creation_date=str(action.creation_date),
            field_name=action.field_name,
            old_value=action.old_value,
            new_value=action.new_value
        ) for action in Actions.select().where(Actions.ticket == ticket.ticket_id)
    ]


def get_ticket_comments(ticket: Tickets):
    return [
        CommentDetailInfoScheme(
            reply_to=CommentBaseDetailInfoSchema(
                comment_id=comment.reply_to.comment_id,
                author=make_short_user_data(
                    comment.author,
                    hide_user_id=(ticket.anonymous and (comment.author.user_id == ticket.creator.user_id))
                ),
                body=comment.reply_to.body,
                creation_date=str(comment.reply_to.creation_date)
            ) if comment.reply_to else None,
            comment_id=comment.comment_id,
            author=make_short_user_data(
                comment.author,
                hide_user_id=(ticket.anonymous and (comment.author.user_id == ticket.creator.user_id))
            ),
            body=comment.body,
            creation_date=str(comment.creation_date)
        ) for comment in Comments.select().where(Comments.ticket == ticket.ticket_id).order_by(
            Comments.creation_date.desc()
        )
    ]
