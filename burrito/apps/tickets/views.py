import math

from fastapi import Depends, status
from fastapi.responses import JSONResponse

from fastapi_jwt_auth import AuthJWT

from burrito.schemas.tickets_schema import (
    CreateTicketSchema,
    TicketIDValueSchema,
    UpdateTicketSchema,
    TicketDetailInfoSchema,
    TicketListRequestSchema,
    TicketListResponseSchema,
    TicketsBasicFilterSchema
)
from burrito.schemas.queue_schema import QueueResponseSchema
from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
from burrito.schemas.pagination_schema import BurritoPagination

from burrito.models.queues_model import Queues
from burrito.models.tickets_model import Tickets
from burrito.models.bookmarks_model import Bookmarks
from burrito.models.deleted_model import Deleted
from burrito.models.liked_model import Liked

from burrito.utils.users_util import get_user_by_id
from burrito.utils.auth_token_util import (
    read_access_token_payload,
    AuthTokenPayload
)
from burrito.utils.query_util import (
    q_is_anonymous,
    q_is_valid_faculty,
    q_is_valid_queue,
    q_is_valid_status_list,
    q_protected_statuses,
    q_not_hidden,
    q_is_hidden,
    q_is_creator,
    q_deleted,
    q_not_deleted,
    q_bookmarked,
    q_liked
)
from burrito.utils.tickets_util import (
    hide_ticket_body,
    make_short_user_data,
    is_ticket_bookmarked,
    get_filtered_tickets,
    select_filters,
    create_ticket_action,
    get_ticket_actions,
    is_ticket_liked
)
from burrito.utils.logger import get_logger
from burrito.utils.converter import (
    FacultyConverter,
    StatusConverter,
    QueueConverter
)

from .utils import (
    get_auth_core,
    is_ticket_exist,
    update_ticket_info,
    check_permission,
    am_i_own_this_ticket,
    am_i_own_this_ticket_with_error,
    make_ticket_detail_info
)


@check_permission(permission_list={"CREATE_TICKET"})
async def tickets__create_new_ticket(
        ticket_creation_data: CreateTicketSchema,
        Authorize: AuthJWT = Depends(get_auth_core())
):
    """Create ticket"""
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    faculty_id = FacultyConverter.convert(ticket_creation_data.faculty)
    queue: Queues = QueueConverter.convert(ticket_creation_data.queue)

    ticket: Tickets = Tickets.create(
        creator=token_payload.user_id,
        subject=ticket_creation_data.subject,
        body=ticket_creation_data.body,
        hidden=ticket_creation_data.hidden,
        anonymous=ticket_creation_data.anonymous,
        queue=queue,
        faculty=faculty_id if faculty_id else get_user_by_id(
            token_payload.user_id
        ).faculty
    )

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Ticket was created successfully",
            "ticket_id": ticket.ticket_id
        }
    )


@check_permission()
async def tickets__delete_ticket_for_me(
        deletion_ticket_data: TicketIDValueSchema,
        Authorize: AuthJWT = Depends(get_auth_core())
):
    """Delete ticket"""
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    ticket: Tickets | None = is_ticket_exist(
        deletion_ticket_data.ticket_id
    )

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
        status_code=200,
        content={"detail": "Ticket was deleted successfully"}
    )


@check_permission()
async def tickets__bookmark_ticket(
        bookmark_ticket_data: TicketIDValueSchema,
        Authorize: AuthJWT = Depends(get_auth_core())
):
    """Follow ticket"""
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    ticket: Tickets | None = is_ticket_exist(
        bookmark_ticket_data.ticket_id
    )

    if ticket.hidden:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": "You have not permission to bookmark this ticket"
            }
        )

    bookmark: Bookmarks | None = Bookmarks.get_or_none(
        Bookmarks.user_id == token_payload.user_id,
        Bookmarks.ticket_id == ticket.ticket_id
    )

    try:
        if not bookmark:
            Bookmarks.create(
                user_id=token_payload.user_id,
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


@check_permission()
async def tickets__unbookmark_ticket(
        unbookmark_ticket_data: TicketIDValueSchema,
        Authorize: AuthJWT = Depends(get_auth_core())
):
    """Follow ticket"""
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    ticket: Tickets | None = is_ticket_exist(
        unbookmark_ticket_data.ticket_id
    )

    bookmark: Bookmarks | None = Bookmarks.get_or_none(
        Bookmarks.user_id == token_payload.user_id,
        Bookmarks.ticket_id == ticket.ticket_id
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


@check_permission()
async def tickets__like_ticket(
        like_ticket_data: TicketIDValueSchema,
        Authorize: AuthJWT = Depends(get_auth_core())
):
    """Like ticket"""
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    ticket: Tickets | None = is_ticket_exist(
        like_ticket_data.ticket_id
    )

    if ticket.hidden:
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


@check_permission()
async def tickets__unlike_ticket(
        unlike_ticket_data: TicketIDValueSchema,
        Authorize: AuthJWT = Depends(get_auth_core())
):
    """Unlike ticket"""
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

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


@check_permission(permission_list={"READ_TICKET"})
async def tickets__show_tickets_list_by_filter(
        filters: TicketListRequestSchema | None = TicketListRequestSchema(),
        Authorize: AuthJWT = Depends(get_auth_core())
):
    """Show tickets"""
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    available_filters = {
        "creator": q_is_creator(filters.creator),
        "hidden": q_is_hidden(filters.hidden),
        "anonymous": q_is_anonymous(filters.anonymous),
        "faculty": q_is_valid_faculty(filters.faculty) if filters.faculty else None,
        "queue": q_is_valid_queue(filters.queue) if filters.queue else None,
        "status": q_is_valid_status_list(filters.status)
    }
    final_filters = select_filters(available_filters, filters) + (
        [
            q_not_deleted(token_payload.user_id)
        ] if filters.creator == token_payload.user_id else [
            q_not_hidden(),
            q_protected_statuses()
        ]
    )

    response_list: list[TicketDetailInfoSchema] = []

    expression: list[Tickets] = get_filtered_tickets(
        final_filters,
        start_page=filters.start_page,
        tickets_count=filters.tickets_count
    )

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
            assignee = make_short_user_data(ticket.assignee, hide_user_id=False)

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
        )).count()/filters.tickets_count)
    )


@check_permission(permission_list={"READ_TICKET"})
async def tickets__show_detail_ticket_info(
        ticket_id_info: TicketIDValueSchema,
        Authorize: AuthJWT = Depends(get_auth_core())
):
    """Show detail ticket info"""
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    ticket: Tickets | None = is_ticket_exist(
        ticket_id_info.ticket_id
    )

    i_am_creator = am_i_own_this_ticket(
        ticket.creator.user_id,
        token_payload.user_id
    )

    if not i_am_creator and ticket.hidden:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Not allowed"}
        )

    creator = None
    if not ticket.anonymous or i_am_creator:
        creator = make_short_user_data(ticket.creator, hide_user_id=False)

    assignee = None
    if ticket.assignee:
        assignee = make_short_user_data(ticket.assignee, hide_user_id=False)

    return make_ticket_detail_info(
        ticket,
        token_payload,
        creator,
        assignee,
        crop_body=False,
        show_history=True
    )


@check_permission()
async def tickets__update_own_ticket_data(
        updates: UpdateTicketSchema,
        Authorize: AuthJWT = Depends(get_auth_core())
):
    """Update ticket info"""
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    ticket: Tickets | None = is_ticket_exist(
        updates.ticket_id
    )

    am_i_own_this_ticket_with_error(
        ticket.creator.user_id,
        token_payload.user_id
    )

    update_ticket_info(ticket, updates)  # autocommit

    return JSONResponse(
        status_code=200,
        content={"detail": "Ticket was updated successfully"}
    )


@check_permission()
async def tickets__close_own_ticket(
        data_to_close_ticket: TicketIDValueSchema,
        Authorize: AuthJWT = Depends(get_auth_core())
):
    """Close ticket"""
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    ticket: Tickets | None = is_ticket_exist(
        data_to_close_ticket.ticket_id
    )

    am_i_own_this_ticket_with_error(
        ticket.creator.user_id,
        token_payload.user_id
    )

    status_id = 6
    status_object = StatusConverter.convert(status_id)

    if not status_object:
        get_logger().critical(f"Status {status_id} is not exist in database")

        return JSONResponse(
            status_code=500,
            content={"detail": "Ticket is not closed. Try latter."}
        )

    create_ticket_action(
        ticket_id=data_to_close_ticket.ticket_id,
        user_id=token_payload.user_id,
        field_name="status",
        old_value=ticket.status.name,
        new_value=status_object.name
    )

    ticket.status = status_object
    ticket.save()

    return JSONResponse(
        status_code=200,
        content={"detail": "Ticket was closed successfully"}
    )


@check_permission()
async def tickets__get_liked_tickets(
        _filters: TicketsBasicFilterSchema | None = TicketsBasicFilterSchema(),
        Authorize: AuthJWT = Depends(get_auth_core())
):
    """Get tickets which were liked by current user"""

    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    available_filters = {
        "hidden": q_is_hidden(_filters.hidden),
        "anonymous": q_is_anonymous(_filters.anonymous),
        "faculty": q_is_valid_faculty(_filters.faculty) if _filters.faculty else None,
        "queue": q_is_valid_queue(_filters.queue) if _filters.queue else None,
        "status": q_is_valid_status_list(_filters.status)
    }
    final_filters = select_filters(available_filters, _filters) + [
        q_liked(token_payload.user_id)
    ]
    expression: list[Tickets] = get_filtered_tickets(
        final_filters,
        start_page=_filters.start_page,
        tickets_count=_filters.tickets_count
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
        total_pages=math.ceil(Liked.select().where(
                Liked.user_id == token_payload.user_id
            ).count()/_filters.tickets_count
        )
    )


@check_permission()
async def tickets__get_bookmarked_tickets(
        _filters: TicketsBasicFilterSchema | None = TicketsBasicFilterSchema(),
        Authorize: AuthJWT = Depends(get_auth_core())
):
    """Get tickets which were bookmarked by current user"""

    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    available_filters = {
        "hidden": q_is_hidden(_filters.hidden),
        "anonymous": q_is_anonymous(_filters.anonymous),
        "faculty": q_is_valid_faculty(_filters.faculty) if _filters.faculty else None,
        "queue": q_is_valid_queue(_filters.queue) if _filters.queue else None,
        "status": q_is_valid_status_list(_filters.status)
    }
    final_filters = select_filters(available_filters, _filters) + [
        q_bookmarked(token_payload.user_id)
    ]
    expression: list[Tickets] = get_filtered_tickets(
        final_filters,
        start_page=_filters.start_page,
        tickets_count=_filters.tickets_count
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
        total_pages=math.ceil(Bookmarks.select().where(
                Bookmarks.user_id == token_payload.user_id
            ).count()/_filters.tickets_count
        )
    )


@check_permission()
async def tickets__get_deleted_tickets(
        _filters: TicketsBasicFilterSchema | None = TicketsBasicFilterSchema(),
        Authorize: AuthJWT = Depends(get_auth_core())
):
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    available_filters = {
        "hidden": q_is_hidden(_filters.hidden),
        "anonymous": q_is_anonymous(_filters.anonymous),
        "faculty": q_is_valid_faculty(_filters.faculty) if _filters.faculty else None,
        "queue": q_is_valid_queue(_filters.queue) if _filters.queue else None,
        "status": q_is_valid_status_list(_filters.status)
    }
    final_filters = select_filters(available_filters, _filters) + [
        q_deleted(token_payload.user_id)
    ]
    expression: list[Tickets] = get_filtered_tickets(
        final_filters,
        start_page=_filters.start_page,
        tickets_count=_filters.tickets_count
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
        )).count()/_filters.tickets_count)
    )
