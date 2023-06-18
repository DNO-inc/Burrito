from fastapi.responses import JSONResponse
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from burrito.schemas.comment_schema import (
    CommentCreationSchema,
    CommentEditSchema,
    CommentDeletionSchema
)

from burrito.models.comments_model import Comments
from burrito.models.tickets_model import Tickets

from burrito.utils.tickets_util import is_ticket_exist
from burrito.utils.permissions_checker import check_permission
from burrito.utils.auth import get_auth_core
from burrito.utils.auth_token_util import (
    AuthTokenPayload,
    read_access_token_payload
)

from .utils import is_comment_exist_with_ext, is_allowed_to_interact


@check_permission()
async def comments__create(
    creation_comment_data: CommentCreationSchema,
    Authorize: AuthJWT = Depends(get_auth_core())
):
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    ticket: Tickets | None = is_ticket_exist(creation_comment_data.ticket_id)
    if ticket.hidden:
        creator_id = ticket.creator.user_id
        assignee_id = ticket.assignee.user_id if ticket.assignee else None

        if token_payload.user_id != creator_id and token_payload.user_id != assignee_id:
            return JSONResponse(
                status_code=403,
                content={
                    "detail": "You have not permissions to create comment here"
                }
            )

    # TODO: add reply_to to this request
    comment: Comments = Comments.create(
        ticket=creation_comment_data.ticket_id,
        author=token_payload.user_id,
        body=creation_comment_data.body
    )

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Comment was created successfully",
            "comment_id": comment.comment_id
        }
    )


@check_permission()
async def comments__edit(
    edit_comment_data: CommentEditSchema,
    Authorize: AuthJWT = Depends(get_auth_core())
):
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    comment: Comments | None = is_comment_exist_with_ext(edit_comment_data.comment_id)
    is_allowed_to_interact(comment, token_payload.user_id)

    if edit_comment_data.body:
        comment.body = edit_comment_data.body

    comment.save()

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Comment was edited successfully"
        }
    )


@check_permission()
async def comments__delete(
    deletion_comment_data: CommentDeletionSchema,
    Authorize: AuthJWT = Depends(get_auth_core())
):
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    comment: Comments | None = is_comment_exist_with_ext(deletion_comment_data.comment_id)
    is_allowed_to_interact(comment, token_payload.user_id)

    comment.delete_instance()

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Comment was deleted successfully"
        }
    )
