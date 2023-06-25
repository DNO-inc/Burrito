import math

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from burrito.models.user_model import Users
from burrito.models.liked_model import Liked
from burrito.models.tickets_model import Tickets
from burrito.models.queues_model import Queues

from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
from burrito.schemas.queue_schema import QueueResponseSchema
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
from burrito.utils.query_util import (
    q_is_anonymous,
    q_is_valid_faculty,
    q_is_valid_queue,
    q_is_valid_status_list,
    q_is_hidden,
)
from burrito.utils.users_util import get_user_by_id
from burrito.utils.tickets_util import (
    hide_ticket_body,
    make_short_user_data,
    is_ticket_bookmarked,
    get_filtered_tickets,
    select_filters,
    create_ticket_action,
    get_ticket_actions
)
from burrito.utils.auth import get_auth_core
from burrito.utils.converter import (
    StatusConverter,
    FacultyConverter,
    QueueConverter
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

    faculty_object = FacultyConverter.convert(admin_updates.faculty)
    if faculty_object:  # faculty_id must be > 1
        create_ticket_action(
            ticket_id=admin_updates.ticket_id,
            author_id=token_payload.user_id,
            field_name="faculty",
            old_value=ticket.faculty.name,
            new_value=faculty_object.name
        )
        ticket.faculty = faculty_object

    queue_object = QueueConverter.convert(admin_updates.queue) if admin_updates.queue else None
    if queue_object:    # queue_id must be > 1
        create_ticket_action(
            ticket_id=admin_updates.ticket_id,
            author_id=token_payload.user_id,
            field_name="queue",
            old_value=ticket.queue.name,
            new_value=queue_object.name
        )
        ticket.queue = queue_object

    current_admin: Users | None = get_user_by_id(token_payload.user_id)
    status_object = None
    if ticket.assignee == current_admin:
        status_object = StatusConverter.convert(admin_updates.status)
        if status_object:    # status_id must be > 1
            create_ticket_action(
                ticket_id=admin_updates.ticket_id,
                author_id=token_payload.user_id,
                field_name="status",
                old_value=ticket.status.name,
                new_value=status_object.name
            )
            ticket.status = status_object

    if any((faculty_object, queue_object, status_object)):
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

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    available_filters = {
        "hidden": q_is_hidden(filters.hidden),
        "anonymous": q_is_anonymous(filters.anonymous),
        "faculty": q_is_valid_faculty(filters.faculty) if filters.faculty else None,
        "queue": q_is_valid_queue(filters.queue) if filters.queue else None,
        "status": q_is_valid_status_list(filters.status)
    }
    final_filters = select_filters(available_filters, filters)

    response_list: list[AdminTicketDetailInfo] = []

    expression: list[Tickets] = get_filtered_tickets(
        final_filters,
        start_page=filters.start_page,
        tickets_count=filters.tickets_count
    )

    for ticket in expression:
        creator = None
        if not ticket.anonymous:
            creator = make_short_user_data(
                ticket.creator,
                hide_user_id=False
            )

        assignee = None
        if ticket.assignee:
            assignee = make_short_user_data(
                ticket.assignee,
                hide_user_id=False
            )

        upvotes = Liked.select().where(
            Liked.ticket_id == ticket.ticket_id
        ).count()

        queue: Queues | None = None
        if ticket.queue:
            queue = Queues.get_or_none(Queues.queue_id == ticket.queue)

        response_list.append(
            AdminTicketDetailInfo(
                creator=creator,
                assignee=assignee,
                ticket_id=ticket.ticket_id,
                subject=ticket.subject,
                body=hide_ticket_body(ticket.body),
                faculty=FacultyResponseSchema(
                    faculty_id=ticket.faculty.faculty_id,
                    name=ticket.faculty.name
                ),
                queue=QueueResponseSchema(
                    queue_id=queue.queue_id,
                    faculty=queue.faculty.faculty_id,
                    name=queue.name,
                    scope=queue.scope
                ) if queue else None,
                status=StatusResponseSchema(
                    status_id=ticket.status.status_id,
                    name=ticket.status.name
                ),
                upvotes=upvotes,
                is_liked=bool(
                    Liked.get_or_none(
                        Liked.user_id == token_payload.user_id,
                        Liked.ticket_id == ticket.ticket_id
                    )
                ),
                is_bookmarked=is_ticket_bookmarked(
                    token_payload.user_id,
                    ticket.ticket_id
                ),
                date=str(ticket.created)
            )
        )

    return AdminTicketListResponse(
        ticket_list=response_list,
        total_pages=math.ceil(Tickets.select().where(*final_filters).count()/filters.tickets_count)
    )


@check_permission()
async def admin__show_detail_ticket_info(
    ticket_id_info: AdminTicketIdSchema,
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

    creator = None
    if not ticket.anonymous:
        creator = make_short_user_data(
            ticket.creator,
            hide_user_id=False
        )

    assignee = None
    if ticket.assignee:
        assignee = make_short_user_data(
            ticket.assignee,
            hide_user_id=False
        )

    queue: Queues | None = None
    if ticket.queue:
        queue = Queues.get_or_none(Queues.queue_id == ticket.queue)

    upvotes = Liked.select().where(
        Liked.ticket_id == ticket.ticket_id
    ).count()

    return AdminTicketDetailInfo(
        creator=creator,
        assignee=assignee,
        ticket_id=ticket.ticket_id,
        subject=ticket.subject,
        body=ticket.body,
        queue=QueueResponseSchema(
            queue_id=queue.queue_id,
            faculty=queue.faculty.faculty_id,
            name=queue.name,
            scope=queue.scope
        ) if queue else None,
        faculty=FacultyResponseSchema(
            faculty_id=ticket.faculty.faculty_id,
            name=ticket.faculty.name
        ),
        status=StatusResponseSchema(
            status_id=ticket.status.status_id,
            name=ticket.status.name
        ),
        upvotes=upvotes,
        is_liked=bool(
            Liked.get_or_none(
                Liked.user_id == token_payload.user_id,
                Liked.ticket_id == ticket.ticket_id
            )
        ),
        is_bookmarked=is_ticket_bookmarked(
            token_payload.user_id,
            ticket.ticket_id
        ),
        date=str(ticket.created),
        history=get_ticket_actions(ticket.ticket_id)
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
        create_ticket_action(
            ticket_id=ticket_data.ticket_id,
            author_id=token_payload.user_id,
            field_name="assignee",
            old_value="None",
            new_value=current_admin.login
        )
        ticket.assignee = current_admin

        new_status = StatusConverter.convert(1)
        create_ticket_action(
            ticket_id=ticket_data.ticket_id,
            author_id=token_payload.user_id,
            field_name="status",
            old_value=ticket.status.name,
            new_value=new_status.name
        )
        ticket.status = new_status

        ticket.save()

    return JSONResponse(
        status_code=200,
        content={"detail": "You are assignee now"}
    )
