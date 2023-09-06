import math

from fastapi import Depends
from fastapi.responses import JSONResponse

from burrito.models.user_model import Users
from burrito.models.tickets_model import Tickets

from burrito.schemas.admin_schema import (
    AdminTicketIdSchema,
    AdminUpdateTicketSchema,
    AdminGetTicketListSchema,
    AdminTicketDetailInfo,
    AdminTicketListResponse
)

from burrito.utils.auth import AuthTokenPayload, BurritoJWT
from burrito.utils.query_util import (
    q_is_anonymous,
    q_is_valid_faculty,
    q_is_valid_queue,
    q_is_valid_status_list,
    q_scope_is,
    q_creator_is,
    q_assignee_is,
    q_is_hidden,
)
from burrito.utils.users_util import get_user_by_id
from burrito.utils.tickets_util import (
    make_short_user_data,
    get_filtered_tickets,
    select_filters,
    create_ticket_action,
)
from burrito.utils.logger import get_logger
from burrito.utils.auth import get_auth_core
from burrito.utils.converter import (
    StatusConverter,
    FacultyConverter,
    QueueConverter
)

from .utils import (
    check_permission,
    is_ticket_exist,
    make_ticket_detail_info
)


async def admin__update_ticket_data(
    admin_updates: AdminUpdateTicketSchema,
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, {"ADMIN"})

    ticket: Tickets | None = is_ticket_exist(
        admin_updates.ticket_id
    )

    faculty_object = FacultyConverter.convert(admin_updates.faculty) if admin_updates.faculty else None
    if faculty_object:  # faculty_id must be > 1
        create_ticket_action(
            ticket_id=admin_updates.ticket_id,
            user_id=token_payload.user_id,
            field_name="faculty",
            old_value=ticket.faculty.name,
            new_value=faculty_object.name
        )
        ticket.faculty = faculty_object

    queue_object = QueueConverter.convert(admin_updates.queue) if admin_updates.queue else None
    if queue_object:    # queue_id must be > 1
        create_ticket_action(
            ticket_id=admin_updates.ticket_id,
            user_id=token_payload.user_id,
            field_name="queue",
            old_value=ticket.queue.name,
            new_value=queue_object.name
        )
        ticket.queue = queue_object

    current_admin: Users | None = get_user_by_id(token_payload.user_id)
    status_object = None
    if ticket.assignee == current_admin:
        status_object = StatusConverter.convert(admin_updates.status) if admin_updates.status else None
        if status_object:    # status_id must be > 1
            create_ticket_action(
                ticket_id=admin_updates.ticket_id,
                user_id=token_payload.user_id,
                field_name="status",
                old_value=ticket.status.name,
                new_value=status_object.name
            )
            ticket.status = status_object

    # changing assignee value
    if admin_updates.assignee_id:  # cause user can give values less
        provided_assignee: Users | None = get_user_by_id(admin_updates.assignee_id)

        # become assignee
        if not ticket.assignee and token_payload.user_id == provided_assignee.user_id:
            create_ticket_action(
                ticket_id=admin_updates.ticket_id,
                user_id=token_payload.user_id,
                field_name="assignee",
                old_value="None",
                new_value=provided_assignee.login
            )
            ticket.assignee = provided_assignee

            new_status = StatusConverter.convert(1)
            create_ticket_action(
                ticket_id=admin_updates.ticket_id,
                user_id=token_payload.user_id,
                field_name="status",
                old_value=ticket.status.name,
                new_value=new_status.name
            )
            ticket.status = new_status

        # forward ticket
        elif ticket.assignee and ticket.assignee.user_id == token_payload.user_id:
            create_ticket_action(
                ticket_id=admin_updates.ticket_id,
                user_id=token_payload.user_id,
                field_name="assignee",
                old_value=ticket.assignee.login,
                new_value=provided_assignee.login
            )
            ticket.assignee = provided_assignee

            new_status = StatusConverter.convert(1)
            create_ticket_action(
                ticket_id=admin_updates.ticket_id,
                user_id=token_payload.user_id,
                field_name="status",
                old_value=ticket.status.name,
                new_value=new_status.name
            )
            ticket.status = new_status

    if any((faculty_object, queue_object, status_object, admin_updates.assignee_id)):
        ticket.save()

    return JSONResponse(
        status_code=200,
        content={"detail": "Ticket data was updated successfully"}
    )


async def admin__get_ticket_list_by_filter(
    filters: AdminGetTicketListSchema | None = AdminGetTicketListSchema(),
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    user_data = check_permission(token_payload, {"ADMIN"})

    available_filters = {
        "ADMIN": [
            q_creator_is(filters.creator),
            q_assignee_is(filters.assignee),
            q_is_hidden(filters.hidden),
            q_is_anonymous(filters.anonymous),
            q_is_valid_faculty(filters.faculty),
            q_is_valid_status_list(filters.status),
            q_scope_is(filters.scope),
            q_is_valid_queue(filters.queue),
        ],
        "default": [
            q_is_hidden(True)
        ]
    }
    final_filters = select_filters(user_data.role_name, available_filters)

    response_list: list[AdminTicketDetailInfo] = []

    expression: list[Tickets] = get_filtered_tickets(
        final_filters,
        start_page=filters.start_page,
        tickets_count=filters.items_count
    )

    for ticket in expression:
        response_list.append(
            make_ticket_detail_info(
                ticket,
                token_payload,
                make_short_user_data(
                    ticket.creator,
                    hide_user_id=False
                ) if not ticket.anonymous else None,
                make_short_user_data(
                    ticket.assignee,
                    hide_user_id=False
                ) if ticket.assignee else None,
                crop_body=True,
                show_history=False
            )
        )

    return AdminTicketListResponse(
        ticket_list=response_list,
        total_pages=math.ceil(
            Tickets.select().where(*final_filters).count()/filters.items_count
        ) if final_filters else math.ceil(Tickets.select().count()/filters.items_count)
    )


async def admin__show_detail_ticket_info(
    ticket_id_info: AdminTicketIdSchema,
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Show detail ticket info"""
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, {"ADMIN"})

    ticket: Tickets | None = is_ticket_exist(
        ticket_id_info.ticket_id
    )

    return make_ticket_detail_info(
        ticket,
        token_payload,
        make_short_user_data(
            ticket.creator,
            hide_user_id=False
        ) if not ticket.anonymous else None,
        make_short_user_data(
            ticket.assignee,
            hide_user_id=False
        ) if ticket.assignee else None,
        crop_body=False
    )


async def admin__delete_ticket(
    deletion_ticket_data: AdminTicketIdSchema,
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, {"ADMIN"})

    ticket: Tickets | None = is_ticket_exist(
        deletion_ticket_data.ticket_id
    )

    get_logger().info(
        f"""
        New deletion (
            ticket_id={ticket.ticket_id},
            initiator={token_payload.user_id}
        )

        """
    )
    ticket.delete_instance()

    return JSONResponse(
        status_code=200,
        content={"detail": "Ticket was deleted successfully"}
    )


async def admin__change_user_permissions():
    return {"1": 1}
