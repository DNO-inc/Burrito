from fastapi.responses import JSONResponse
from fastapi import Depends

from burrito.schemas.comment_schema import (
    CommentCreationSchema,
    CommentEditSchema,
    CommentDeletionSchema,
    RequestTicketsCommentSchema,
    ResponseTicketsCommentSchema,
    CommentDetailInfoScheme
)

from burrito.models.comments_model import Comments
from burrito.models.tickets_model import Tickets

from burrito.utils.tickets_util import is_ticket_exist
from burrito.utils.permissions_checker import check_permission
from burrito.utils.auth import get_auth_core
from burrito.utils.auth import AuthTokenPayload, BurritoJWT


from .utils import (
    is_comment_exist_with_error,
    is_allowed_to_interact,
    make_short_comment_author_info
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


async def comments__edit(
    edit_comment_data: CommentEditSchema,
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, {"SEND_MESSAGE"})

    comment: Comments | None = is_comment_exist_with_error(edit_comment_data.comment_id)
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


async def comments__delete(
    deletion_comment_data: CommentDeletionSchema,
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, {"SEND_MESSAGE"})

    comment: Comments | None = is_comment_exist_with_error(deletion_comment_data.comment_id)
    is_allowed_to_interact(comment, token_payload.user_id)

    comment.delete_instance()

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Comment was deleted successfully"
        }
    )


async def comments__get_related_comments(
    filters: RequestTicketsCommentSchema,
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Obtain comments related to the ticket"""

    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, {"SEND_MESSAGE"})

    ticket: Tickets | None = is_ticket_exist(filters.ticket_id)
    if ticket.hidden:
        creator_id = ticket.creator.user_id
        assignee_id = ticket.assignee.user_id if ticket.assignee else None

        if token_payload.user_id not in (creator_id, assignee_id):
            return JSONResponse(
                status_code=403,
                content={
                    "detail": "You have not permissions to get comments"
                }
            )

    return ResponseTicketsCommentSchema(
        ticket_id=filters.ticket_id,
        comment_list=[
            CommentDetailInfoScheme(
                comment_id=comment.comment_id,
                author=make_short_comment_author_info(
                    comment.author,
                    hide_user_id=ticket.anonymous and comment.author.user_id == ticket.creator.user_id
                ),
                body=comment.body,
                comment_date=str(comment.comment_date)
            ) for comment in Comments.select().where(Comments.ticket == filters.ticket_id).paginate(
                filters.start_page,
                filters.items_count
            ).order_by(
                Comments.comment_date.desc()
            )
        ]
    )
