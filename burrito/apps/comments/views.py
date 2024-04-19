from fastapi.responses import JSONResponse
from fastapi import Depends

from burrito.schemas.comment_schema import (
    CommentCreationSchema,
    CommentEditSchema,
    CommentIDSchema,
    CommentBaseDetailInfoSchema,
    CommentDetailInfoScheme
)

from burrito.models.m_notifications_model import Notifications
from burrito.models.m_comments_model import Comments
from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users

from burrito.utils.mongo_util import mongo_insert, mongo_update, mongo_delete
from burrito.utils.tickets_util import (
    is_ticket_exist,
    am_i_own_this_ticket,
    send_notification,
    make_short_user_data,
    send_comment_update
)
from burrito.utils.auth import get_current_user
from burrito.utils.query_util import STATUS_OPEN
from burrito.utils.tickets_util import create_ticket_action, can_i_interact_with_ticket

from .utils import (
    is_comment_exist_with_error,
    is_allowed_to_interact
)


async def comments__create(
    creation_comment_data: CommentCreationSchema,
    _curr_user: Users = Depends(get_current_user(permission_list={"SEND_MESSAGE"}))
):
    ticket: Tickets | None = is_ticket_exist(creation_comment_data.ticket_id)

    if not can_i_interact_with_ticket(ticket, _curr_user.user_id):
        return JSONResponse(
            status_code=403,
            content={
                "detail": "Permission denied"
            }
        )

    comment_id: str = mongo_insert(
        Comments(
            reply_to=creation_comment_data.reply_to,
            ticket_id=creation_comment_data.ticket_id,
            author_id=_curr_user.user_id,
            body=creation_comment_data.body
        )
    )

    send_notification(
        ticket,
        Notifications(
            ticket_id=ticket.ticket_id,
            user_id=_curr_user.user_id,
            body_ua=f"Хтось створив новий коментарій у зверненні {ticket.ticket_id}",
            body=f"Someone has created a new comment in ticket {ticket.ticket_id}"
        ),
        author_id=_curr_user.user_id
    )
    send_comment_update(ticket.ticket_id, comment_id, msg_type="MSG_CREATE")

    if ticket.status.status_id in (4, 6) and am_i_own_this_ticket(ticket.creator.user_id, _curr_user.user_id):
        create_ticket_action(
            ticket_id=ticket.ticket_id,
            user_id=_curr_user.user_id,
            field_name="status",
            old_value=ticket.status.name,
            new_value=STATUS_OPEN.name
        )
        ticket.status = STATUS_OPEN
        ticket.save()

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Comment was created successfully",
            "comment_id": comment_id
        }
    )


async def comments__edit(
    edit_comment_data: CommentEditSchema,
    _curr_user: Users = Depends(get_current_user(permission_list={"SEND_MESSAGE"}))
):
    comment: Comments | None = is_comment_exist_with_error(edit_comment_data.comment_id)
    is_allowed_to_interact(comment, _curr_user.user_id)

    if edit_comment_data.body:
        comment["body"] = edit_comment_data.body
        comment_id = comment["_id"]

        mongo_update(
            Comments(**comment),
            _id=comment_id
        )

    ticket: Tickets | None = is_ticket_exist(comment["ticket_id"])

    send_comment_update(ticket.ticket_id, str(comment["_id"]), msg_type="MSG_EDIT")

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Comment was edited successfully"
        }
    )


async def comments__delete(
    deletion_comment_data: CommentIDSchema,
    _curr_user: Users = Depends(get_current_user(permission_list={"SEND_MESSAGE"}))
):
    comment: Comments | None = is_comment_exist_with_error(deletion_comment_data.comment_id)
    is_allowed_to_interact(comment, _curr_user.user_id)

    mongo_delete(Comments, _id=comment["_id"])

    ticket: Tickets | None = is_ticket_exist(comment["ticket_id"])

    send_comment_update(ticket.ticket_id, str(comment["_id"]), msg_type="MSG_DELETE")

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Comment was deleted successfully"
        }
    )


async def comments__get_comment_by_id(
    comment_data: CommentIDSchema,
    _curr_user: Users = Depends(get_current_user(permission_list={"SEND_MESSAGE"}))
):
    comment: Comments | None = is_comment_exist_with_error(comment_data.comment_id)

    ticket: Tickets = is_ticket_exist(comment["ticket_id"])

    if not can_i_interact_with_ticket(ticket, _curr_user.user_id):
        return JSONResponse(
            status_code=403,
            content={
                "detail": "Permission denied"
            }
        )

    additional_data = is_comment_exist_with_error(comment["reply_to"]) if comment["reply_to"] else None

    ticket_owner = am_i_own_this_ticket(ticket.creator.user_id, _curr_user.user_id)

    return CommentDetailInfoScheme(
        reply_to=CommentBaseDetailInfoSchema(
            comment_id=str(additional_data["_id"]),
            author=make_short_user_data(
                additional_data["author_id"],
                hide_user_id=False if ticket_owner else (ticket.anonymous and (additional_data["author_id"] == ticket.creator.user_id))
            ),
            body=additional_data["body"],
            creation_date=additional_data["creation_date"]
        ) if additional_data else None,
        comment_id=str(comment["_id"]),
        author=make_short_user_data(
            comment["author_id"],
            hide_user_id=False if ticket_owner else (ticket.anonymous and (comment["author_id"] == ticket.creator.user_id))
        ),
        body=comment["body"],
        creation_date=comment["creation_date"]
    )
