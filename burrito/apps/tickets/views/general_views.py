from fastapi import Depends
from fastapi.responses import JSONResponse

from burrito.models.queues_model import Queues
from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users
from burrito.schemas.tickets_schema import (
    CreateTicketSchema,
    TicketIDValueSchema,
    UpdateTicketSchema,
)
from burrito.utils.auth import get_current_user
from burrito.utils.converter import DivisionConverter, QueueConverter
from burrito.utils.logger import get_logger
from burrito.utils.query_util import STATUS_CLOSE
from burrito.utils.tickets_util import create_ticket_action
from burrito.utils.users_util import get_user_by_id

from ..utils import am_i_own_this_ticket_with_error, is_ticket_exist, update_ticket_info


async def tickets__create_new_ticket(
        ticket_creation_data: CreateTicketSchema,
        _curr_user: Users = Depends(get_current_user())
):
    """Create ticket"""

    division_id = DivisionConverter.convert(ticket_creation_data.division)
    queue: Queues = QueueConverter.convert(ticket_creation_data.queue)

    # TODO: use _curr_user.division instead
    division = division_id if division_id else get_user_by_id(
        _curr_user.user_id
    ).division

    ticket: Tickets = Tickets.create(
        creator=_curr_user.user_id,
        subject=ticket_creation_data.subject.strip(),
        body=ticket_creation_data.body.strip(),
        hidden=ticket_creation_data.hidden,
        anonymous=ticket_creation_data.anonymous,
        queue=queue,
        division=division
    )

    get_logger().info(
        f"""
        New ticket (
            ticket_id={ticket.ticket_id},
            creator={_curr_user.user_id},
            subject={ticket_creation_data.subject},
            hidden={ticket_creation_data.hidden},
            anonymous={ticket_creation_data.anonymous},
            queue={queue},
            division={division}
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
        _curr_user: Users = Depends(get_current_user())
):
    """Update ticket info"""

    ticket: Tickets | None = is_ticket_exist(
        updates.ticket_id
    )

    am_i_own_this_ticket_with_error(
        ticket.creator.user_id,
        _curr_user.user_id
    )

    update_ticket_info(ticket, updates)  # autocommit

    return JSONResponse(
        status_code=200,
        content={"detail": "Ticket was updated successfully"}
    )


async def tickets__close_own_ticket(
        data_to_close_ticket: TicketIDValueSchema,
        _curr_user: Users = Depends(get_current_user())
):
    """Close ticket"""

    ticket: Tickets | None = is_ticket_exist(
        data_to_close_ticket.ticket_id
    )

    am_i_own_this_ticket_with_error(
        ticket.creator.user_id,
        _curr_user.user_id
    )

    create_ticket_action(
        ticket_id=data_to_close_ticket.ticket_id,
        user_id=_curr_user.user_id,
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
