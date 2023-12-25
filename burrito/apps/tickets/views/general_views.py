from fastapi import Depends
from fastapi.responses import JSONResponse

from burrito.schemas.tickets_schema import (
    CreateTicketSchema,
    TicketIDValueSchema,
    UpdateTicketSchema
)

from burrito.models.queues_model import Queues
from burrito.models.tickets_model import Tickets

from burrito.utils.users_util import get_user_by_id
from burrito.utils.auth import AuthTokenPayload, BurritoJWT

from burrito.utils.tickets_util import create_ticket_action
from burrito.utils.logger import get_logger
from burrito.utils.query_util import STATUS_CLOSE
from burrito.utils.converter import (
    FacultyConverter,
    QueueConverter
)

from ..utils import (
    get_auth_core,
    is_ticket_exist,
    update_ticket_info,
    check_permission,
    am_i_own_this_ticket_with_error
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


__all__ = [i for i in dir() if i.startswith("tickets__")]
