import math

from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse

from burrito.schemas.tickets_schema import (
    CreateTicketSchema,
    TicketIDValueSchema,
    UpdateTicketSchema,
    TicketDetailInfoSchema,
    TicketListRequestSchema,
    TicketListResponseSchema,
    TicketsBasicFilterSchema,
    TicketIDValuesListScheme,
    BaseFilterSchema,
    RequestTicketHistorySchema
)
from burrito.schemas.action_schema import RequestActionSchema, ActionSchema, FileActionSchema

from burrito.models.queues_model import Queues
from burrito.models.tickets_model import Tickets
from burrito.models.bookmarks_model import Bookmarks
from burrito.models.deleted_model import Deleted
from burrito.models.liked_model import Liked
from burrito.models.m_actions_model import Actions
from burrito.models.m_actions_model import BaseAction

from burrito.utils.users_util import get_user_by_id, get_user_by_id_or_none
from burrito.utils.auth import AuthTokenPayload, BurritoJWT
from burrito.utils.mongo_util import mongo_select
from burrito.utils.query_util import (
    q_is_anonymous,
    q_is_valid_faculty,
    q_is_valid_queue,
    q_scope_is,
    q_is_valid_status_list,
    q_not_hidden,
    q_owned_or_not_hidden,
    q_protected_statuses,
    q_not_deleted,
    q_is_hidden,
    q_assignee_is,
    q_deleted,
    q_bookmarked,
    q_followed,
    q_liked,
    q_creator_is,
    STATUS_CLOSE,
    ADMIN_ROLES
)
from burrito.utils.tickets_util import (
    make_short_user_data,
    get_filtered_tickets,
    select_filters,
    create_ticket_action,
    get_ticket_history,
    can_i_interact_with_ticket
)
from burrito.utils.mongo_util import mongo_page_count
from burrito.utils.logger import get_logger
from burrito.utils.converter import (
    FacultyConverter,
    QueueConverter
)

from .utils import (
    get_auth_core,
    is_ticket_exist,
    update_ticket_info,
    check_permission,
    am_i_own_this_ticket,
    am_i_own_this_ticket_with_error,
    make_ticket_detail_info,
    get_filtered_bookmarks,
    get_filtered_bookmarks_count
)


async def tickets__create_new_ticket(
        ticket_creation_data: CreateTicketSchema,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Create ticket"""

    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, permission_list={"CREATE_TICKET"})

    faculty_id = FacultyConverter.convert(ticket_creation_data.faculty)
    queue: Queues = QueueConverter.convert(ticket_creation_data.queue)

    faculty = faculty_id if faculty_id else get_user_by_id(
        token_payload.user_id
    ).faculty

    ticket: Tickets = Tickets.create(
        creator=token_payload.user_id,
        subject=ticket_creation_data.subject.strip(),
        body=ticket_creation_data.body.strip(),
        hidden=ticket_creation_data.hidden,
        anonymous=ticket_creation_data.anonymous,
        queue=queue,
        faculty=faculty
    )

    get_logger().info(
        f"""
        New ticket (
            ticket_id={ticket.ticket_id},
            creator={token_payload.user_id},
            subject={ticket_creation_data.subject},
            hidden={ticket_creation_data.hidden},
            anonymous={ticket_creation_data.anonymous},
            queue={queue},
            faculty={faculty}
        )

        """
    )

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Ticket was created successfully",
            "ticket_id": ticket.ticket_id
        }
    )


async def tickets__delete_ticket_for_me(
        deletion_ticket_data: TicketIDValuesListScheme,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Delete ticket"""

    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload)

    for id_value in deletion_ticket_data.ticket_id_list:
        ticket: Tickets | None = is_ticket_exist(id_value)

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
                status_code=500,
                content={"detail": "Something went wrong"}
            )

    return JSONResponse(
        status_code=200,
        content={"detail": "Tickets were deleted successfully"}
    )


async def tickets__undelete_ticket(
        ticket_data: TicketIDValueSchema,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload)

    ticket: Tickets | None = is_ticket_exist(ticket_data.ticket_id)

    am_i_own_this_ticket_with_error(
        ticket.creator.user_id,
        token_payload.user_id
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


async def tickets__bookmark_ticket(
        bookmark_ticket_data: TicketIDValueSchema,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Follow ticket"""
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload)

    current_user = get_user_by_id(token_payload.user_id)

    ticket: Tickets | None = is_ticket_exist(
        bookmark_ticket_data.ticket_id
    )

    if not can_i_interact_with_ticket(ticket, current_user):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": "You have not permission to bookmark this ticket"
            }
        )

    bookmark: Bookmarks | None = Bookmarks.get_or_none(
        Bookmarks.user == token_payload.user_id,
        Bookmarks.ticket == ticket.ticket_id
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


async def tickets__unbookmark_ticket(
        unbookmark_ticket_data: TicketIDValueSchema,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Follow ticket"""
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload)

    ticket: Tickets | None = is_ticket_exist(
        unbookmark_ticket_data.ticket_id
    )

    bookmark: Bookmarks | None = Bookmarks.get_or_none(
        Bookmarks.user == token_payload.user_id,
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


async def tickets__like_ticket(
        like_ticket_data: TicketIDValueSchema,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Like ticket"""
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload)

    current_user = get_user_by_id(token_payload.user_id)

    ticket: Tickets | None = is_ticket_exist(
        like_ticket_data.ticket_id
    )

    if not can_i_interact_with_ticket(ticket, current_user):
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


async def tickets__unlike_ticket(
        unlike_ticket_data: TicketIDValueSchema,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Unlike ticket"""
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload)

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


async def tickets__show_tickets_list_by_filter(
        filters: TicketListRequestSchema | None = TicketListRequestSchema(),
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Show tickets"""
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    user_data = check_permission(token_payload, permission_list={"READ_TICKET"})

    available_filters = {
        "default": [
            q_creator_is(filters.creator) if filters.creator else None,
            q_assignee_is(filters.assignee),
            q_is_hidden(filters.hidden),
            q_is_anonymous(filters.anonymous),
            q_is_valid_faculty(filters.faculty),
            q_is_valid_status_list(filters.status),
            q_scope_is(filters.scope),
            q_is_valid_queue(filters.queue),
            *([
                q_not_deleted(token_payload.user_id)
            ] if filters.creator == token_payload.user_id else [
                q_not_hidden(),
                q_protected_statuses()
            ])
        ]
    }
    final_filters = select_filters(user_data.role_name, available_filters)
    expression: list[Tickets] = get_filtered_tickets(
        final_filters,
        start_page=filters.start_page,
        tickets_count=filters.items_count
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
        )).count()/filters.items_count)
    )


async def tickets__show_detail_ticket_info(
        ticket_id_info: TicketIDValueSchema,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Show detail ticket info"""
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, permission_list={"READ_TICKET"})

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
        crop_body=False
    )


async def tickets__update_own_ticket_data(
        updates: UpdateTicketSchema,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Update ticket info"""
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload)

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


async def tickets__close_own_ticket(
        data_to_close_ticket: TicketIDValueSchema,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Close ticket"""
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload)

    ticket: Tickets | None = is_ticket_exist(
        data_to_close_ticket.ticket_id
    )

    am_i_own_this_ticket_with_error(
        ticket.creator.user_id,
        token_payload.user_id
    )

    create_ticket_action(
        ticket_id=data_to_close_ticket.ticket_id,
        user_id=token_payload.user_id,
        field_name="status",
        old_value=ticket.status.name,
        new_value=STATUS_CLOSE.name
    )

    ticket.status = STATUS_CLOSE
    ticket.save()

    return JSONResponse(
        status_code=200,
        content={"detail": "Ticket was closed successfully"}
    )


async def tickets__get_liked_tickets(
        _filters: TicketsBasicFilterSchema | None = TicketsBasicFilterSchema(),
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Get tickets which were liked by current user"""

    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    user_data = check_permission(token_payload)

    available_filters = {
        "default": [
            q_owned_or_not_hidden(token_payload.user_id, _filters.hidden),
            q_is_anonymous(_filters.anonymous),
            q_is_valid_faculty(_filters.faculty),
            q_is_valid_status_list(_filters.status),
            q_scope_is(_filters.scope),
            q_is_valid_queue(_filters.queue),
            q_liked(token_payload.user_id)
        ]
    }
    final_filters = select_filters(user_data.role_name, available_filters)
    expression: list[Tickets] = get_filtered_tickets(
        final_filters,
        start_page=_filters.start_page,
        tickets_count=_filters.items_count
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
        total_pages=math.ceil(Tickets.select().where(*(
            final_filters
        )).count()/_filters.items_count) if final_filters else math.ceil(Tickets.select().count()/_filters.items_count)
    )


async def tickets__get_bookmarked_tickets(
        _filters: TicketsBasicFilterSchema | None = TicketsBasicFilterSchema(),
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Get tickets which were bookmarked by current user"""

    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    user_data = check_permission(token_payload)

    available_filters = {
        "default": [
            q_is_anonymous(_filters.anonymous),
            q_is_valid_faculty(_filters.faculty),
            q_is_valid_status_list(_filters.status),
            q_scope_is(_filters.scope),
            q_is_valid_queue(_filters.queue),
            q_bookmarked(token_payload.user_id)
        ]
    }
    final_filters = select_filters(user_data.role_name, available_filters)
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
                token_payload,
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
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Get tickets which were followed by current user"""

    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    user_data = check_permission(token_payload)

    available_filters = {
        "default": [
            q_not_hidden(),
            q_is_anonymous(_filters.anonymous),
            q_is_valid_faculty(_filters.faculty),
            q_is_valid_status_list(_filters.status),
            q_scope_is(_filters.scope),
            q_is_valid_queue(_filters.queue),
            q_followed(token_payload.user_id),
            q_protected_statuses()
        ]
    }
    final_filters = select_filters(user_data.role_name, available_filters)
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
                token_payload,
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


async def tickets__get_deleted_tickets(
        _filters: TicketsBasicFilterSchema | None = TicketsBasicFilterSchema(),
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    user_data = check_permission(token_payload)

    available_filters = {
        "default": [
            q_is_anonymous(_filters.anonymous),
            q_is_valid_faculty(_filters.faculty),
            q_is_valid_status_list(_filters.status),
            q_scope_is(_filters.scope),
            q_is_valid_queue(_filters.queue),
            q_deleted(token_payload.user_id)
        ]
    }
    final_filters = select_filters(user_data.role_name, available_filters)

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
        )).count()/_filters.items_count)
    )


async def tickets__get_full_ticket_history(
        _filters: RequestTicketHistorySchema,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload)

    ticket = is_ticket_exist(_filters.ticket_id)

    if not can_i_interact_with_ticket(ticket, token_payload.user_id):
        return JSONResponse(
            status_code=403,
            content={
                "detail": "Permission denied"
            }
        )

    history = get_ticket_history(
        ticket,
        token_payload.user_id,
        start_page=_filters.start_page,
        items_count=_filters.items_count
    )

    return {
        "history": history,
        "page_count": mongo_page_count(Actions, items_count=_filters.items_count, ticket_id=ticket.ticket_id)
    }


async def tickets__get_action_by_id(
        action_data: RequestActionSchema,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload)

    action = mongo_select(BaseAction, _id=action_data.action_id)

    if action:
        action = action[0]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Action with action_id {action_data.action_id} is not exists"
        )

    if not action.get("type_"):
        raise HTTPException(
            status_code=404,
            detail=f"Action with action_id {action_data.action_id} is not exists"
        )

    if action["type_"] != "action":
        raise HTTPException(
            status_code=404,
            detail=f"Action with action_id {action_data.action_id} is not exists"
        )

    ticket: Tickets = is_ticket_exist(action["ticket_id"])
    ticket_owner = am_i_own_this_ticket(ticket.ticket_id, token_payload.user_id)
    if not can_i_interact_with_ticket(ticket, token_payload.user_id):
        raise HTTPException(
            status_code=403,
            detail="Forbidden to interact with this ticket"
        )

    if action["field_name"] == "file":
        return FileActionSchema(
            ticket_id=action["ticket_id"],
            author=make_short_user_data(
                action["user_id"],
                hide_user_id=False if ticket_owner else (ticket.anonymous and (action["user_id"] == ticket.creator.user_id))
            ),
            creation_date=action["creation_date"],
            field_name=action["field_name"],
            value=action["value"]
        )

    # if it's regular action
    old_value = action["old_value"]
    new_value = action["new_value"]

    if action["field_name"] == "assignee":
        old_assignee = get_user_by_id_or_none(action["old_value"])
        new_assignee = get_user_by_id_or_none(action["new_value"])

        old_value = old_assignee.login if old_assignee else action["old_value"]
        new_value = new_assignee.login if new_assignee else action["new_value"]

    return ActionSchema(
        ticket_id=action["ticket_id"],
        author=make_short_user_data(
            action["user_id"],
            hide_user_id=False if ticket_owner else (ticket.anonymous and (action["user_id"] == ticket.creator.user_id))
        ),
        creation_date=action["creation_date"],
        field_name=action["field_name"],
        old_value=old_value,
        new_value=new_value
    )
