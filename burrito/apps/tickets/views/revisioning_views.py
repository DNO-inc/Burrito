import math

from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse

from burrito.schemas.tickets_schema import (
    TicketIDValueSchema,
    TicketDetailInfoSchema,
    TicketListRequestSchema,
    TicketListResponseSchema,
    RequestTicketHistorySchema
)
from burrito.schemas.action_schema import RequestActionSchema, ActionSchema, FileActionSchema

from burrito.models.tickets_model import Tickets
from burrito.models.m_actions_model import Actions
from burrito.models.m_actions_model import BaseAction

from burrito.utils.users_util import get_user_by_id_or_none
from burrito.utils.auth import AuthTokenPayload, BurritoJWT
from burrito.utils.mongo_util import mongo_select
from burrito.utils.query_util import (
    q_is_anonymous,
    q_is_valid_faculty,
    q_is_valid_queue,
    q_scope_is,
    q_is_valid_status_list,
    q_not_hidden,
    q_protected_statuses,
    q_not_deleted,
    q_is_hidden,
    q_assignee_is,
    q_creator_is
)
from burrito.utils.tickets_util import (
    make_short_user_data,
    get_filtered_tickets,
    select_filters,
    get_ticket_history,
    can_i_interact_with_ticket
)
from burrito.utils.mongo_util import mongo_page_count

from ..utils import (
    get_auth_core,
    is_ticket_exist,
    check_permission,
    am_i_own_this_ticket,
    make_ticket_detail_info
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
            value=action["value"],
            file_meta_action=action["file_meta_action"]
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


__all__ = [i for i in dir() if i.startswith("tickets__")]
