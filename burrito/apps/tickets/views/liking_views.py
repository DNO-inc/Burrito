import math

from fastapi import Depends, status
from fastapi.responses import JSONResponse

from burrito.schemas.tickets_schema import (
    TicketIDValueSchema,
    TicketDetailInfoSchema,
    TicketListResponseSchema,
    TicketsBasicFilterSchema
)

from burrito.models.tickets_model import Tickets
from burrito.models.liked_model import Liked

from burrito.utils.users_util import get_user_by_id
from burrito.utils.auth import AuthTokenPayload, BurritoJWT
from burrito.utils.query_util import (
    q_is_anonymous,
    q_is_valid_faculty,
    q_is_valid_queue,
    q_scope_is,
    q_is_valid_status_list,
    q_owned_or_not_hidden,
    q_liked
)
from burrito.utils.tickets_util import (
    make_short_user_data,
    get_filtered_tickets,
    select_filters,
    can_i_interact_with_ticket
)
from burrito.utils.logger import get_logger

from ..utils import (
    get_auth_core,
    is_ticket_exist,
    check_permission,
    am_i_own_this_ticket,
    make_ticket_detail_info
)


async def tickets__like_ticket(
        like_ticket_data: TicketIDValueSchema,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Like ticket"""
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload)

    current_user = get_user_by_id(token_payload.user_id)

    ticket: Tickets | None = is_ticket_exist(
        like_ticket_data.ticket_id
    )

    if not can_i_interact_with_ticket(ticket, current_user):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": "You have not permission to follow this ticket"
            }
        )

    like: Liked | None = Liked.get_or_none(
        Liked.user_id == token_payload.user_id,
        Liked.ticket_id == ticket.ticket_id
    )

    try:
        if not like:
            Liked.create(
                user_id=token_payload.user_id,
                ticket_id=ticket.ticket_id
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Ticket was liked successfully"}
        )

    except Exception as e:  # pylint: disable=broad-except, invalid-name
        get_logger().critical(f"Ticket liking error: {e}")

    # if like already exist
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "detail": "Ticked liking error, is this ticket already liked?"
        }
    )


async def tickets__unlike_ticket(
        unlike_ticket_data: TicketIDValueSchema,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Unlike ticket"""
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload)

    ticket: Tickets | None = is_ticket_exist(
        unlike_ticket_data.ticket_id
    )

    like: Liked | None = Liked.get_or_none(
        Liked.user_id == token_payload.user_id,
        Liked.ticket_id == ticket.ticket_id
    )

    if like:
        like.delete_instance()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Ticket unliked successfully"}
        )

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "This ticket is not liked"}
    )


async def tickets__get_liked_tickets(
        _filters: TicketsBasicFilterSchema | None = TicketsBasicFilterSchema(),
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Get tickets which were liked by current user"""

    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    user_data = check_permission(token_payload)

    available_filters = {
        "default": [
            q_owned_or_not_hidden(token_payload.user_id, _filters.hidden),
            q_is_anonymous(_filters.anonymous),
            q_is_valid_faculty(_filters.faculty),
            q_is_valid_status_list(_filters.status),
            q_scope_is(_filters.scope),
            q_is_valid_queue(_filters.queue),
            q_liked(token_payload.user_id)
        ]
    }
    final_filters = select_filters(user_data.role_name, available_filters)
    expression: list[Tickets] = get_filtered_tickets(
        final_filters,
        start_page=_filters.start_page,
        tickets_count=_filters.items_count
    )

    response_list: list[TicketDetailInfoSchema] = []
    for ticket in expression:
        i_am_creator = am_i_own_this_ticket(
            ticket.creator.user_id,
            token_payload.user_id
        )

        if not i_am_creator and ticket.hidden:
            continue

        creator = None
        if not ticket.anonymous or i_am_creator:
            creator = make_short_user_data(ticket.creator, hide_user_id=False)

        assignee = None
        if ticket.assignee:
            assignee = make_short_user_data(
                ticket.assignee,
                hide_user_id=False
            )

        response_list.append(
            make_ticket_detail_info(
                ticket,
                token_payload,
                creator,
                assignee,
                crop_body=True
            )
        )

    return TicketListResponseSchema(
        ticket_list=response_list,
        total_pages=math.ceil(Tickets.select().where(*(
            final_filters
        )).count()/_filters.items_count) if final_filters else math.ceil(Tickets.select().count()/_filters.items_count)
    )


__all__ = [i for i in dir() if i.startswith("tickets__")]
