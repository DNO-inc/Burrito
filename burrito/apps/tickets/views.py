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

    faculty_id = FacultyStrToInt.convert(ticket_creation_data.faculty)
    if not faculty_id:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Faculty name is wrong"}
        )

    ticket: Tickets = Tickets.create(
        creator=Authorize.get_jwt_subject(),
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

    ticket: Tickets | None = is_ticket_exist(
        deletion_ticket_data.ticket_id
    )

    am_i_own_this_ticket_with_error(
        ticket.creator.user_id,
        Authorize.get_jwt_subject()
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

    ticket: Tickets | None = is_ticket_exist(
        bookmark_ticket_data.ticket_id
    )

    try:
        Bookmarks.create(
            user_id=Authorize.get_jwt_subject(),
            ticket_id=ticket.ticket_id
        )
    except Exception as e:  # pylint: disable=broad-except, invalid-name
        get_logger().critical(f"Creation error: {e}")

    return JSONResponse(
        status_code=200,
        content={"detail": "Ticket was bookmarked successfully"}
    )


@check_permission(permission_list={"READ_TICKET"})
async def tickets__show_tickets_list_by_filter(
    filters: TicketListRequestSchema,
    Authorize: AuthJWT = Depends(get_auth_core())
):
    """Show tickets"""
    Authorize.jwt_required()

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

    for item in Deleted.select().where(Deleted.user_id == Authorize.get_jwt_subject()):
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
            Authorize.get_jwt_subject()
        )

        if not i_am_creator and ticket.hidden:
            continue

        if ticket.ticket_id in tickets_black_list:
            continue

        creator = None
        assignee = None
        if not ticket.anonymous or i_am_creator:
            creator = model_to_dict(ticket.creator)
            creator["faculty"] = ticket.creator.faculty.name

            assignee = ticket.assignee
            assignee_modified = dict()
            if assignee:
                assignee_modified = model_to_dict(assignee)
                assignee_modified["faculty"] = ticket.assignee.faculty.name

        response_list.append(
            TicketDetailInfoSchema(
                creator=creator,
                assignee=assignee_modified if assignee else None,
                ticket_id=ticket.ticket_id,
                subject=ticket.subject,
                body=hide_ticket_body(ticket.body),
                faculty=ticket.faculty.name,
                status=ticket.status.name
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

    ticket: Tickets | None = is_ticket_exist(
        ticket_id_info.ticket_id
    )

    i_am_creator = am_i_own_this_ticket(
        ticket.creator.user_id,
        Authorize.get_jwt_subject()
    )

    if not i_am_creator and ticket.hidden:
        return JSONResponse(
            status_code=403,
            content={"detail": "Not allowed"}
        )

    creator = None
    if not ticket.anonymous:
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

    return TicketDetailInfoSchema(
        creator=creator,
        assignee=assignee,
        ticket_id=ticket.ticket_id,
        subject=ticket.subject,
        body=ticket.body,
        faculty=ticket.faculty.name,
        status=ticket.status.name
    )


@check_permission()
async def tickets__update_own_ticket_data(
    updates: UpdateTicketSchema,
    Authorize: AuthJWT = Depends(get_auth_core())
):
    """Update ticket info"""
    Authorize.jwt_required()

    ticket: Tickets | None = is_ticket_exist(
        updates.ticket_id
    )

    am_i_own_this_ticket_with_error(
        ticket.creator.user_id,
        Authorize.get_jwt_subject()
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

    ticket: Tickets | None = is_ticket_exist(
        data_to_close_ticket.ticket_id
    )

    am_i_own_this_ticket_with_error(
        ticket.creator.user_id,
        Authorize.get_jwt_subject()
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
