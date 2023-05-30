from fastapi import Depends, status
from fastapi.responses import JSONResponse

from fastapi_jwt_auth import AuthJWT

from playhouse.shortcuts import model_to_dict

from burrito.schemas.tickets_schema import (
    CreateTicketSchema,
    TicketIDValueSchema,
    UpdateTicketSchema,
    TicketDetailInfoSchema,
    TicketListRequestSchema,
    TicketListResponseSchema
)
from burrito.models.tickets_model import Tickets
from burrito.models.bookmarks_model import Bookmarks
from burrito.models.deleted_model import Deleted
from burrito.models.liked_model import Liked

from burrito.utils.auth_token_util import (
    read_access_token_payload,
    AuthTokenPayload
)
from burrito.utils.tickets_util import hide_ticket_body
from burrito.utils.logger import get_logger
from burrito.utils.converter import (
    QueueStrToInt,
    FacultyStrToInt,
    StatusStrToInt
)

from .utils import (
    get_auth_core,
    is_ticket_exist,
    update_ticket_info,
    check_permission,
    am_i_own_this_ticket,
    am_i_own_this_ticket_with_error
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

    faculty_id = FacultyStrToInt.convert(ticket_creation_data.faculty)
    if not faculty_id:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Faculty name is wrong"}
        )

    ticket: Tickets = Tickets.create(
        creator=token_payload.user_id,
        subject=ticket_creation_data.subject,
        body=ticket_creation_data.body,
        hidden=ticket_creation_data.hidden,
        anonymous=ticket_creation_data.anonymous,
        queue=QueueStrToInt.convert(ticket_creation_data.queue),
        faculty=faculty_id
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
        content={"detail": "Ticked liking error, is this ticket already liked?"}
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
    filters: TicketListRequestSchema,
    Authorize: AuthJWT = Depends(get_auth_core())
):
    """Show tickets"""
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    available_filters = {
        "creator": Tickets.creator == filters.creator,
        "hidden": Tickets.hidden == filters.hidden,
        "anonymous": Tickets.anonymous == filters.anonymous,
        "faculty": Tickets.faculty == FacultyStrToInt.convert(filters.faculty),
        "queue": Tickets.queue == QueueStrToInt.convert(filters.queue),
        "status": Tickets.status == StatusStrToInt.convert(filters.status)
    }

    final_filters = []
    for filter_item in filters.dict().items():
        if filter_item[1] is not None:
            final_filters.append(available_filters[filter_item[0]])

    response_list: TicketDetailInfoSchema = []

    tickets_black_list = set()

    for item in Deleted.select().where(Deleted.user_id == token_payload.user_id):
        tickets_black_list.add(item.ticket_id.ticket_id)

    expression = None
    if final_filters:
        expression = Tickets.select().where(*final_filters)
    else:
        # TODO: make pagination
        expression = Tickets.select()

    for ticket in expression:
        i_am_creator = am_i_own_this_ticket(
            ticket.creator.user_id,
            token_payload.user_id
        )

        if not i_am_creator and ticket.hidden:
            continue

        if i_am_creator:
            if ticket.ticket_id in tickets_black_list:
                continue

        creator = None
        if not ticket.anonymous or i_am_creator:
            creator = model_to_dict(ticket.creator)
            creator["faculty"] = ticket.creator.faculty.name

        assignee = ticket.assignee
        assignee_modified: dict = {}
        if assignee:
            assignee_modified = model_to_dict(assignee)
            assignee_modified["faculty"] = ticket.assignee.faculty.name

        upvotes = Liked.select().where(
            Liked.ticket_id == ticket.ticket_id
        ).count()

        response_list.append(
            TicketDetailInfoSchema(
                creator=creator,
                assignee=assignee_modified if assignee else None,
                ticket_id=ticket.ticket_id,
                subject=ticket.subject,
                body=hide_ticket_body(ticket.body, 500),
                faculty=ticket.faculty.name,
                status=ticket.status.name,
                upvotes=upvotes
            )
        )

    return TicketListResponseSchema(
        ticket_list=response_list
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
        creator = model_to_dict(ticket.creator)

        try:
            creator["faculty"] = ticket.creator.faculty.name
        except:
            get_logger().critical(
                f"User {ticket.creator.user_id} without faculty value"
            )
            creator["faculty"] = None

    assignee = ticket.assignee
    assignee_modified = dict()
    if assignee:
        assignee_modified = model_to_dict(assignee)

        try:
            assignee_modified["faculty"] = ticket.assignee.faculty.name
        except:
            get_logger().critical(
                f"User {ticket.assignee} without faculty value"
            )
            assignee_modified["faculty"] = None

    upvotes = Liked.select().where(
        Liked.ticket_id == ticket.ticket_id
    ).count()

    return TicketDetailInfoSchema(
        creator=creator,
        assignee=assignee,
        ticket_id=ticket.ticket_id,
        subject=ticket.subject,
        body=ticket.body,
        faculty=ticket.faculty.name,
        status=ticket.status.name,
        upvotes=upvotes
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

    status_name = "CLOSE"
    status_object = StatusStrToInt.convert(status_name)

    if not status_object:
        get_logger().critical(f"Status {status_name} is not exist in database")

        return JSONResponse(
            status_code=500,
            content={"detail": "Ticket is not closed. Try latter."}
        )

    ticket.status = status_object
    ticket.save()

    return JSONResponse(
        status_code=200,
        content={"detail": "Ticket was closed successfully"}
    )
