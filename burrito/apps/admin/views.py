import math

from fastapi import Depends, status
from fastapi.responses import JSONResponse

from burrito.models.m_comments_model import Comments
from burrito.models.m_ticket_files import TicketFiles
from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users
from burrito.schemas.admin_schema import (
    AdminGetTicketListSchema,
    AdminTicketDetailInfo,
    AdminTicketIdSchema,
    AdminTicketListResponse,
    AdminUpdateTicketSchema,
)
from burrito.schemas.profile_schema import AdminRequestUpdateProfileSchema
from burrito.utils.auth import get_current_user
from burrito.utils.converter import DivisionConverter, QueueConverter, StatusConverter
from burrito.utils.logger import get_logger
from burrito.utils.mongo_util import mongo_delete, mongo_delete_file, mongo_select
from burrito.utils.query_util import (
    q_assignee_is,
    q_creator_is,
    q_followed,
    q_is_anonymous,
    q_is_hidden,
    q_is_valid_division,
    q_is_valid_queue,
    q_is_valid_status_list,
    q_scope_is,
)
from burrito.utils.tickets_util import (
    am_i_own_this_ticket,
    change_ticket_assignee,
    change_ticket_division,
    change_ticket_queue,
    change_ticket_status,
    get_filtered_bookmarks,
    get_filtered_bookmarks_count,
    get_filtered_tickets,
    make_short_user_data,
    select_filters,
)
from burrito.utils.users_util import get_user_by_id

from .utils import is_ticket_exist, make_ticket_detail_info, update_profile_as_admin


async def admin__update_ticket_data(
    admin_updates: AdminUpdateTicketSchema,
    _curr_user: Users = Depends(get_current_user(permission_list={"ADMIN"}))
):
    ticket: Tickets | None = is_ticket_exist(
        admin_updates.ticket_id
    )

    division_object = DivisionConverter.convert(admin_updates.division_id) if admin_updates.division_id else None
    if division_object:
        change_ticket_division(ticket, _curr_user.user_id, division_object)

    queue_object = QueueConverter.convert(admin_updates.queue) if admin_updates.queue else None
    if queue_object:
        change_ticket_queue(ticket, _curr_user.user_id, queue_object)

    status_object = None
    if ticket.assignee and ticket.assignee.user_id == _curr_user.user_id:
        status_object = StatusConverter.convert(admin_updates.status) if admin_updates.status else None
        if status_object and ticket.queue:
            change_ticket_status(ticket, _curr_user.user_id, status_object)

    if admin_updates.assignee_id:
        change_ticket_assignee(
            ticket,
            _curr_user.user_id,
            get_user_by_id(admin_updates.assignee_id) if admin_updates.assignee_id >= 0 else None
        )

    if any((division_object, queue_object, status_object, admin_updates.assignee_id)):
        ticket.save()

    return JSONResponse(
        status_code=200,
        content={"detail": "Ticket data was updated successfully"}
    )


async def admin__get_ticket_list_by_filter(
    filters: AdminGetTicketListSchema | None = AdminGetTicketListSchema(),
    _curr_user: Users = Depends(get_current_user(permission_list={"ADMIN"}))
):
    admin_filters = [
        q_creator_is(filters.creator),
        q_assignee_is(filters.assignee),
        q_is_hidden(filters.hidden),
        q_is_anonymous(filters.anonymous),
        q_is_valid_division(filters.division_id),
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
    final_filters = select_filters(_curr_user.role.name, available_filters)

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
                _curr_user,
                make_short_user_data(
                    ticket.creator,
                    hide_user_id=False
                ) if not ticket.anonymous or am_i_own_this_ticket(
                    ticket.creator.user_id,
                    _curr_user.user_id
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
    _curr_user: Users = Depends(get_current_user(permission_list={"ADMIN"}))
):
    """Show detail ticket info"""

    ticket: Tickets | None = is_ticket_exist(
        ticket_id_info.ticket_id
    )

    return make_ticket_detail_info(
        ticket,
        _curr_user,
        make_short_user_data(
            ticket.creator,
            hide_user_id=False
        ) if not ticket.anonymous or am_i_own_this_ticket(
            ticket.creator.user_id,
            _curr_user.user_id
        ) else None,
        make_short_user_data(
            ticket.assignee,
            hide_user_id=False
        ) if ticket.assignee else None,
        crop_body=False
    )


async def admin__delete_ticket(
    deletion_ticket_data: AdminTicketIdSchema,
    _curr_user: Users = Depends(get_current_user(permission_list={"ADMIN"}))
):
    ticket: Tickets | None = is_ticket_exist(
        deletion_ticket_data.ticket_id
    )

    get_logger().info(
        f"""
        New deletion (
            ticket_id={ticket.ticket_id},
            initiator={_curr_user.user_id}
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
    _curr_user: Users = Depends(get_current_user(permission_list={"ADMIN"}))
):
    if profile_updated_data.user_id in (None, _curr_user.user_id):
        await update_profile_as_admin(
            _curr_user.user_id,
            profile_updated_data,
            allow_extra_fields=False
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Profile was updated"}
        )

    current_user = get_user_by_id(_curr_user.user_id)
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


async def admin__get_followed_tickets(
    _filters: AdminGetTicketListSchema | None = AdminGetTicketListSchema(),
    _curr_user: Users = Depends(get_current_user(permission_list={"ADMIN"}))
):
    admin_filters = [
        q_is_hidden(_filters.hidden),
        q_is_anonymous(_filters.anonymous),
        q_is_valid_division(_filters.division_id),
        q_is_valid_status_list(_filters.status),
        q_scope_is(_filters.scope),
        q_is_valid_queue(_filters.queue),
        q_followed(_curr_user.user_id)
    ]

    available_filters = {
        "ADMIN": admin_filters,
        "CHIEF_ADMIN": admin_filters,
        "default": [
            q_is_hidden(False)
        ]
    }
    final_filters = select_filters(_curr_user.role.name, available_filters)
    expression: list[Tickets] = get_filtered_bookmarks(
        final_filters,
        start_page=_filters.start_page,
        tickets_count=_filters.items_count
    )

    response_list: list[AdminTicketDetailInfo] = []
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

    return AdminTicketListResponse(
        ticket_list=response_list,
        total_pages=math.ceil(
            get_filtered_bookmarks_count(
                final_filters,
                start_page=_filters.start_page,
                tickets_count=_filters.items_count
            ) / _filters.items_count
        )
    )
