import math

from fastapi import Depends, status
from fastapi.responses import JSONResponse

from burrito.schemas.tickets_schema import (
    TicketDetailInfoSchema,
    TicketListResponseSchema,
    TicketsBasicFilterSchema,
    BaseFilterSchema,
)

from burrito.models.tickets_model import Tickets
from burrito.models.bookmarks_model import Bookmarks

from burrito.utils.users_util import get_user_by_id
from burrito.utils.auth import get_current_user
from burrito.utils.query_util import (
    q_is_anonymous,
    q_is_valid_faculty,
    q_is_valid_queue,
    q_scope_is,
    q_is_valid_status_list,
    q_not_hidden,
    q_protected_statuses,
    q_bookmarked,
    q_followed
)
from burrito.utils.tickets_util import (
    make_short_user_data,
    select_filters,
    can_i_interact_with_ticket
)
from burrito.utils.logger import get_logger

from ..utils import (
    is_ticket_exist,
    make_ticket_detail_info,
    get_filtered_bookmarks,
    get_filtered_bookmarks_count
)


async def tickets__bookmark_ticket(
        ticket_id: int,
        _curr_user=Depends(get_current_user())
):
    """Follow ticket"""

    current_user = get_user_by_id(_curr_user.user_id)

    ticket: Tickets | None = is_ticket_exist(ticket_id)

    if not can_i_interact_with_ticket(ticket, current_user):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": "You have not permission to bookmark this ticket"
            }
        )

    bookmark: Bookmarks | None = Bookmarks.get_or_none(
        Bookmarks.user == _curr_user.user_id,
        Bookmarks.ticket == ticket.ticket_id
    )

    try:
        if not bookmark:
            Bookmarks.create(
                user_id=_curr_user.user_id,
                ticket_id=ticket.ticket_id
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Ticket was bookmarked successfully"}
        )

    except Exception as e:  # pylint: disable=broad-except, invalid-name
        get_logger().critical(f"Bookmark creation error: {e}")

    # if bookmark already exist
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "Bookmark creation error, is this ticket already bookmarked?"}
    )


async def tickets__unbookmark_ticket(
        ticket_id: int,
        _curr_user=Depends(get_current_user())
):
    """Follow ticket"""

    ticket: Tickets | None = is_ticket_exist(ticket_id)

    bookmark: Bookmarks | None = Bookmarks.get_or_none(
        Bookmarks.user == _curr_user.user_id,
        Bookmarks.ticket == ticket.ticket_id
    )

    if bookmark:
        bookmark.delete_instance()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Bookmark for this ticket was successfully deleted"}
        )

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "This ticket is not bookmarked"}
    )


async def tickets__get_bookmarked_tickets(
        _filters: TicketsBasicFilterSchema | None = TicketsBasicFilterSchema(),
        _curr_user=Depends(get_current_user())
):
    """Get tickets which were bookmarked by current user"""

    available_filters = {
        "default": [
            q_is_anonymous(_filters.anonymous),
            q_is_valid_faculty(_filters.faculty),
            q_is_valid_status_list(_filters.status),
            q_scope_is(_filters.scope),
            q_is_valid_queue(_filters.queue),
            q_bookmarked(_curr_user.user_id)
        ]
    }
    final_filters = select_filters(_curr_user.role.name, available_filters)
    expression: list[Tickets] = get_filtered_bookmarks(
        final_filters,
        start_page=_filters.start_page,
        tickets_count=_filters.items_count
    )

    response_list: list[TicketDetailInfoSchema] = []
    for ticket in expression:
        assignee = None
        if ticket.assignee:
            assignee = make_short_user_data(
                ticket.assignee,
                hide_user_id=False
            )

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
        total_pages=math.ceil(
            get_filtered_bookmarks_count(
                final_filters,
                start_page=_filters.start_page,
                tickets_count=_filters.items_count
            ) / _filters.items_count
        )
    )


async def tickets__get_followed_tickets(
        _filters: BaseFilterSchema | None = BaseFilterSchema(),
        _curr_user=Depends(get_current_user())
):
    """Get tickets which were followed by current user"""

    available_filters = {
        "default": [
            q_not_hidden(),
            q_is_anonymous(_filters.anonymous),
            q_is_valid_faculty(_filters.faculty),
            q_is_valid_status_list(_filters.status),
            q_scope_is(_filters.scope),
            q_is_valid_queue(_filters.queue),
            q_followed(_curr_user.user_id),
            q_protected_statuses()
        ]
    }
    final_filters = select_filters(_curr_user.role.name, available_filters)
    expression: list[Tickets] = get_filtered_bookmarks(
        final_filters,
        start_page=_filters.start_page,
        tickets_count=_filters.items_count
    )

    response_list: list[TicketDetailInfoSchema] = []
    for ticket in expression:
        creator = None
        if not ticket.anonymous:
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
                _curr_user,
                creator,
                assignee,
                crop_body=True
            )
        )

    return TicketListResponseSchema(
        ticket_list=response_list,
        total_pages=math.ceil(
            get_filtered_bookmarks_count(
                final_filters,
                start_page=_filters.start_page,
                tickets_count=_filters.items_count
            ) / _filters.items_count
        )
    )


__all__ = [i for i in dir() if i.startswith("tickets__")]
