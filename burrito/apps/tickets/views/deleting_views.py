import math

from fastapi import Depends
from fastapi.responses import JSONResponse

from burrito.schemas.tickets_schema import (
    TicketIDValueSchema,
    TicketListResponseSchema,
    TicketsBasicFilterSchema,
    TicketIDValuesListScheme
)
from burrito.models.tickets_model import Tickets
from burrito.models.deleted_model import Deleted

from burrito.utils.auth import AuthTokenPayload, BurritoJWT
from burrito.utils.tickets_util import (
    am_i_own_this_ticket_with_error,
    select_filters,
    get_filtered_tickets,
    make_short_user_data
)
from burrito.utils.logger import get_logger
from burrito.utils.query_util import (
    q_is_anonymous,
    q_is_valid_faculty,
    q_is_valid_queue,
    q_scope_is,
    q_is_valid_status_list,
    q_deleted
)

from ..utils import (
    get_auth_core,
    is_ticket_exist,
    check_permission,
    make_ticket_detail_info
)


async def tickets__delete_ticket_for_me(
        deletion_ticket_data: TicketIDValuesListScheme,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Delete ticket"""

    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload)

    for id_value in deletion_ticket_data.ticket_id_list:
        ticket: Tickets | None = is_ticket_exist(id_value)

        am_i_own_this_ticket_with_error(
            ticket.creator.user_id,
            token_payload.user_id
        )

        try:
            Deleted.create(
                user_id=ticket.creator.user_id,
                ticket_id=ticket.ticket_id
            )
        except Exception as e:  # pylint: disable=broad-except, invalid-name
            get_logger().critical(f"Creation error: {e}")

            return JSONResponse(
                status_code=500,
                content={"detail": "Something went wrong"}
            )

    return JSONResponse(
        status_code=200,
        content={"detail": "Tickets were deleted successfully"}
    )


async def tickets__undelete_ticket(
        ticket_data: TicketIDValueSchema,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload)

    ticket: Tickets | None = is_ticket_exist(ticket_data.ticket_id)

    am_i_own_this_ticket_with_error(
        ticket.creator.user_id,
        token_payload.user_id
    )

    try:
        # delete ticket from black list
        Deleted.get(Deleted.ticket_id == ticket.ticket_id).delete_instance()

    except Exception as e:
        get_logger().critical(f"Deletion error: {e}")

        return JSONResponse(
            status_code=500,
            content={"detail": "Something went wrong"}
        )

    return JSONResponse(
        status_code=200,
        content={"detail": "Ticket was deleted from black list successfully"}
    )


async def tickets__get_deleted_tickets(
        _filters: TicketsBasicFilterSchema | None = TicketsBasicFilterSchema(),
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    user_data = check_permission(token_payload)

    available_filters = {
        "default": [
            q_is_anonymous(_filters.anonymous),
            q_is_valid_faculty(_filters.faculty),
            q_is_valid_status_list(_filters.status),
            q_scope_is(_filters.scope),
            q_is_valid_queue(_filters.queue),
            q_deleted(token_payload.user_id)
        ]
    }
    final_filters = select_filters(user_data.role_name, available_filters)

    expression: list[Tickets] = get_filtered_tickets(
        final_filters,
        start_page=_filters.start_page,
        tickets_count=_filters.items_count
    )

    response_list: list = []
    for ticket in expression:
        assignee = None
        if ticket.assignee:
            assignee = make_short_user_data(ticket.assignee, hide_user_id=False)

        response_list.append(
            make_ticket_detail_info(
                ticket,
                token_payload,
                make_short_user_data(ticket.creator, hide_user_id=False),
                assignee,
                crop_body=True
            )
        )

    return TicketListResponseSchema(
        ticket_list=response_list,
        total_pages=math.ceil(Tickets.select().where(*(
            final_filters
        )).count()/_filters.items_count)
    )


__all__ = [i for i in dir() if i.startswith("tickets__")]
