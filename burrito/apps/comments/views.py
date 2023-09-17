from fastapi.responses import JSONResponse
from fastapi import Depends

from burrito.schemas.comment_schema import (
    CommentCreationSchema,
    CommentEditSchema,
    CommentDeletionSchema
)

from burrito.models.m_comments_model import Comments
from burrito.models.tickets_model import Tickets

from burrito.utils.mongo_util import mongo_insert, mongo_update, mongo_delete
from burrito.utils.tickets_util import is_ticket_exist
from burrito.utils.permissions_checker import check_permission
from burrito.utils.auth import get_auth_core
from burrito.utils.auth import AuthTokenPayload, BurritoJWT
from burrito.utils.query_util import STATUS_OPEN
from burrito.utils.tickets_util import create_ticket_action

from .utils import (
    is_comment_exist_with_error,
    is_allowed_to_interact
)


async def comments__create(
    creation_comment_data: CommentCreationSchema,
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, {"SEND_MESSAGE"})

    ticket: Tickets | None = is_ticket_exist(creation_comment_data.ticket_id)
    if ticket.hidden:
        creator_id = ticket.creator.user_id
        assignee_id = ticket.assignee.user_id if ticket.assignee else None

        if token_payload.user_id not in (creator_id, assignee_id):
            return JSONResponse(
                status_code=403,
                content={
                    "detail": "You have not permissions to create comment here"
                }
            )

    comment: str = mongo_insert(
        Comments(
            reply_to=creation_comment_data.reply_to,
            ticket_id=creation_comment_data.ticket_id,
            author_id=token_payload.user_id,
            body=creation_comment_data.body
        )
    )

    if ticket.status.status_id in (4, 6):
        create_ticket_action(
            ticket_id=ticket.ticket_id,
            user_id=token_payload.user_id,
            field_name="status",
            old_value=ticket.status.name,
            new_value=STATUS_OPEN.name
        )
        ticket.status = STATUS_OPEN

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Comment was created successfully",
            "comment_id": comment
        }
    )


async def comments__edit(
    edit_comment_data: CommentEditSchema,
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, {"SEND_MESSAGE"})

    comment: Comments | None = is_comment_exist_with_error(edit_comment_data.comment_id)
    is_allowed_to_interact(comment, token_payload.user_id)

    if edit_comment_data.body:
        comment["body"] = edit_comment_data.body
        comment_id = comment["_id"]

        mongo_update(
            Comments(**comment),
            _id=comment_id
        )

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Comment was edited successfully"
        }
    )


async def comments__delete(
    deletion_comment_data: CommentDeletionSchema,
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, {"SEND_MESSAGE"})

    comment: Comments | None = is_comment_exist_with_error(deletion_comment_data.comment_id)
    is_allowed_to_interact(comment, token_payload.user_id)

    mongo_delete(Comments, _id=comment["_id"])

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Comment was deleted successfully"
        }
    )
