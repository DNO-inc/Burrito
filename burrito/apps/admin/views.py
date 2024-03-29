import math

from fastapi import Depends, status
from fastapi.responses import JSONResponse

from burrito.models.tickets_model import Tickets

from burrito.schemas.profile_schema import AdminRequestUpdateProfileSchema
from burrito.schemas.admin_schema import (
    AdminTicketIdSchema,
    AdminUpdateTicketSchema,
    AdminGetTicketListSchema,
    AdminTicketDetailInfo,
    AdminTicketListResponse
)

from burrito.models.m_comments_model import Comments
from burrito.models.m_ticket_files import TicketFiles

from burrito.utils.auth import AuthTokenPayload, BurritoJWT
from burrito.utils.query_util import (
    q_is_anonymous,
    q_is_valid_faculty,
    q_is_valid_queue,
    q_is_valid_status_list,
    q_scope_is,
    q_creator_is,
    q_assignee_is,
    q_is_hidden
)
from burrito.utils.users_util import get_user_by_id
from burrito.utils.mongo_util import (
    mongo_delete,
    mongo_select,
    mongo_delete_file
)
from burrito.utils.tickets_util import (
    make_short_user_data,
    get_filtered_tickets,
    select_filters,
    change_ticket_status,
    change_ticket_faculty,
    change_ticket_queue,
    change_ticket_assignee,
    am_i_own_this_ticket
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
    make_ticket_detail_info,
    update_profile_as_admin
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
    if faculty_object:
        change_ticket_faculty(ticket, token_payload.user_id, faculty_object)

    queue_object = QueueConverter.convert(admin_updates.queue) if admin_updates.queue else None
    if queue_object:
        change_ticket_queue(ticket, token_payload.user_id, queue_object)

    status_object = None
    if ticket.assignee and ticket.assignee.user_id == token_payload.user_id:
        status_object = StatusConverter.convert(admin_updates.status) if admin_updates.status else None
        if status_object and ticket.queue:
            change_ticket_status(ticket, token_payload.user_id, status_object)

    if admin_updates.assignee_id:
        change_ticket_assignee(
            ticket,
            token_payload.user_id,
            get_user_by_id(admin_updates.assignee_id) if admin_updates.assignee_id >= 0 else None
        )

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

    admin_filters = [
        q_creator_is(filters.creator),
        q_assignee_is(filters.assignee),
        q_is_hidden(filters.hidden),
        q_is_anonymous(filters.anonymous),
        q_is_valid_faculty(filters.faculty),
        q_is_valid_status_list(filters.status),
        q_scope_is(filters.scope),
        q_is_valid_queue(filters.queue)
    ]

    available_filters = {
        "ADMIN": admin_filters,
        "CHIEF_ADMIN": admin_filters,
        "default": [
            q_is_hidden(False)
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
                ) if not ticket.anonymous or am_i_own_this_ticket(
                    ticket.creator.user_id,
                    token_payload.user_id
                ) else None,
                make_short_user_data(
                    ticket.assignee,
                    hide_user_id=False
                ) if ticket.assignee else None,
                crop_body=True
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
        ) if not ticket.anonymous or am_i_own_this_ticket(
            ticket.creator.user_id,
            token_payload.user_id
        ) else None,
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

    # delete comments
    mongo_delete(
        Comments,
        ticket_id=deletion_ticket_data.ticket_id
    )

    # delete files
    file_objects = mongo_select(
        TicketFiles,
        ticket_id=deletion_ticket_data.ticket_id
    )
    for file_metadata in file_objects:
        mongo_delete_file(file_metadata.get("file_id"))

    # delete files metadata
    mongo_delete(
        TicketFiles,
        ticket_id=deletion_ticket_data.ticket_id
    )

    return JSONResponse(
        status_code=200,
        content={"detail": "Ticket was deleted successfully"}
    )


async def admin__update_profile(
    profile_updated_data: AdminRequestUpdateProfileSchema = AdminRequestUpdateProfileSchema(),
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, {"ADMIN"})

    if profile_updated_data.user_id in (None, token_payload.user_id):
        await update_profile_as_admin(
            token_payload.user_id,
            profile_updated_data,
            allow_extra_fields=False
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Profile was updated"}
        )

    current_user = get_user_by_id(token_payload.user_id)
    target_user = get_user_by_id(profile_updated_data.user_id)

    # TODO: this is a temporary solution while field 'priority' has not added to Roles model
    if (
        current_user.role.role_id > target_user.role.role_id
        and current_user.role.role_id > profile_updated_data.role_id
    ):
        await update_profile_as_admin(
            profile_updated_data.user_id,
            profile_updated_data,
            allow_extra_fields=True
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Profile was updated"}
        )

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "It's prohibited to update this profile"}
    )
