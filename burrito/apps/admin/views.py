from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from playhouse.shortcuts import model_to_dict

from burrito.models.user_model import Users
from burrito.models.tickets_model import Tickets

from burrito.schemas.admin_schema import (
    AdminTicketIdSchema,
    AdminUpdateTicketSchema,
    AdminGetTicketListSchema,
    AdminTicketDetailInfo,
    AdminTicketListResponse
)

from burrito.utils.auth_token_util import (
    read_access_token_payload,
    AuthTokenPayload
)
from burrito.utils.users_util import get_user_by_id
from burrito.utils.tickets_util import hide_ticket_body
from burrito.utils.auth import get_auth_core
from burrito.utils.converter import (
    StatusStrToModel,
    FacultyStrToModel,
    QueueStrToModel
)

from .utils import (
    check_permission,
    is_ticket_exist
)


@check_permission()
async def admin__update_ticket_data(
    admin_updates: AdminUpdateTicketSchema,
    Authorize: AuthJWT = Depends(get_auth_core())
):
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    ticket: Tickets | None = is_ticket_exist(
        admin_updates.ticket_id
    )

    faculty_id = FacultyStrToModel.convert(admin_updates.faculty)
    if faculty_id:  # faculty_id must be > 1
        ticket.faculty = faculty_id

    queue_id = QueueStrToModel.convert(admin_updates.queue, admin_updates.faculty)
    if queue_id:    # queue_id must be > 1
        ticket.queue = queue_id

    current_admin: Users | None = get_user_by_id(token_payload.user_id)
    status_id = 0
    if ticket.assignee == current_admin:
        status_id = StatusStrToModel.convert(admin_updates.status)
        if status_id:    # status_id must be > 1
            ticket.status = status_id

    if any((faculty_id, queue_id, status_id)):
        ticket.save()

    return JSONResponse(
        status_code=200,
        content={"detail": "Ticket data was updated successfully"}
    )


@check_permission()
async def admin__get_ticket_list_by_filter(
    filters: AdminGetTicketListSchema,
    Authorize: AuthJWT = Depends(get_auth_core())
):
    Authorize.jwt_required()

    available_filters = {
        "hidden": Tickets.hidden == filters.hidden,
        "anonymous": Tickets.anonymous == filters.anonymous,
        "faculty": Tickets.faculty == FacultyStrToModel.convert(filters.faculty),
        "queue": Tickets.queue == QueueStrToModel.convert(filters.queue, filters.faculty),
        "status": Tickets.status == StatusStrToModel.convert(filters.status)
    }

    final_filters = []

    for filter_item in filters.dict().items():
        if filter_item[1] is not None:
            final_filters.append(available_filters[filter_item[0]])

    response_list: AdminTicketDetailInfo = []

    expression = None
    if final_filters:
        expression = Tickets.select().where(*final_filters)
    else:
        # TODO: make pagination
        expression = Tickets.select()

    for ticket in expression:
        creator = None
        assignee = None
        if not ticket.anonymous:
            creator = model_to_dict(ticket.creator)
            creator["faculty"] = ticket.creator.faculty.name

            assignee = ticket.assignee
            assignee_modified = dict()
            if assignee:
                assignee_modified = model_to_dict(assignee)
                assignee_modified["faculty"] = ticket.assignee.faculty.name

        response_list.append(
            AdminTicketDetailInfo(
                creator=creator,
                assignee=assignee_modified if assignee else None,
                ticket_id=ticket.ticket_id,
                subject=ticket.subject,
                body=hide_ticket_body(ticket.body),
                faculty=ticket.faculty.name,
                status=ticket.status.name
            )
        )

    return AdminTicketListResponse(
        ticket_list=response_list
    )


@check_permission()
async def admin__show_detail_ticket_info(
    ticket_id_info: AdminTicketIdSchema,
    Authorize: AuthJWT = Depends(get_auth_core())
):
    """Show detail ticket info"""
    Authorize.jwt_required()

    ticket: Tickets | None = is_ticket_exist(
        ticket_id_info.ticket_id
    )

    creator = None
    if not ticket.anonymous:
        creator = model_to_dict(ticket.creator)
        creator["faculty"] = ticket.creator.faculty.name
        creator["group"] = ticket.creator.group.name

    assignee = ticket.assignee
    if assignee:
        assignee = model_to_dict(assignee)
        assignee["faculty"] = ticket.assignee.faculty.name
        assignee["group"] = ticket.assignee.group.name

    return AdminTicketDetailInfo(
        creator=creator,
        assignee=assignee,
        ticket_id=ticket.ticket_id,
        subject=ticket.subject,
        body=ticket.body,
        queue=ticket.queue.name if ticket.queue else None,
        faculty=ticket.faculty.name,
        status=ticket.status.name
    )


@check_permission()
async def admin__delete_ticket(
    deletion_ticket_data: AdminTicketIdSchema,
    Authorize: AuthJWT = Depends(get_auth_core())
):
    Authorize.jwt_required()

    ticket: Tickets | None = is_ticket_exist(
        deletion_ticket_data.ticket_id
    )

    ticket.delete_instance()

    return JSONResponse(
        status_code=200,
        content={"detail": "Ticket was deleted successfully"}
    )


@check_permission()
async def admin__change_user_permissions():
    return {"1": 1}


@check_permission()
async def admin__become_an_assignee(
    ticket_data: AdminTicketIdSchema,
    Authorize: AuthJWT = Depends(get_auth_core())
):
    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    ticket: Tickets | None = is_ticket_exist(
        ticket_data.ticket_id
    )

    if not ticket.assignee:
        current_admin: Users | None = get_user_by_id(
            token_payload.user_id
        )
        ticket.assignee = current_admin
        ticket.status = StatusStrToModel.convert("OPEN")

        ticket.save()

    return JSONResponse(
        status_code=200,
        content={"detail": "You are assignee now"}
    )
