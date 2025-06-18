import math

from fastapi import Depends
from fastapi.responses import JSONResponse

from burrito.models.deleted_model import Deleted
from burrito.models.tickets_model import Tickets
from burrito.schemas.tickets_schema import (
    TicketIDValueSchema,
    TicketIDValuesListScheme,
    TicketListResponseSchema,
    TicketsBasicFilterSchema,
)
from burrito.utils.auth import get_current_user
from burrito.utils.logger import get_logger
from burrito.utils.query_util import (
    q_deleted,
    q_is_anonymous,
    q_is_valid_division,
    q_is_valid_queue,
    q_is_valid_status_list,
    q_scope_is,
)
from burrito.utils.tickets_util import (
    am_i_own_this_ticket_with_error,
    get_filtered_tickets,
    make_short_user_data,
    select_filters,
)

from ..utils import is_ticket_exist, make_ticket_detail_info


async def tickets__delete_ticket_for_me(
        deletion_ticket_data: TicketIDValuesListScheme,
        _curr_user=Depends(get_current_user())
):
    """Delete ticket"""

    for id_value in deletion_ticket_data.ticket_id_list:
        ticket: Tickets | None = is_ticket_exist(id_value)

        am_i_own_this_ticket_with_error(
            ticket.creator.user_id,
            _curr_user.user_id
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
        _curr_user=Depends(get_current_user())
):
    ticket: Tickets | None = is_ticket_exist(ticket_data.ticket_id)

    am_i_own_this_ticket_with_error(
        ticket.creator.user_id,
        _curr_user.user_id
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
        _curr_user=Depends(get_current_user())
):
    available_filters = {
        "default": [
            q_is_anonymous(_filters.anonymous),
            q_is_valid_division(_filters.division),
            q_is_valid_status_list(_filters.status),
            q_scope_is(_filters.scope),
            q_is_valid_queue(_filters.queue),
            q_deleted(_curr_user.user_id)
        ]
    }
    final_filters = select_filters(_curr_user.role.name, available_filters)

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
                _curr_user,
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
