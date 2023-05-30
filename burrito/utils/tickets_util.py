from fastapi import HTTPException, status

from burrito.models.tickets_model import Tickets


def is_ticket_exist(ticket_id: int) -> Tickets | None:
    """_summary_

    Args:
        ticket_id (int): ticket ID

    Returns:
        Tickets | None: return ticket object if exist else return None
    """

    _ticket = Tickets.get_or_none(
        Tickets.ticket_id == ticket_id
    )

    if not _ticket:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"ticket_id {ticket_id} is not exist"
        )

    return _ticket


def am_i_own_this_ticket(ticket_creator_id: int, user_id: int) -> bool:
    return ticket_creator_id == user_id


def am_i_own_this_ticket_with_error(
    ticket_creator_id: int, user_id: int
) -> bool | None:
    if not am_i_own_this_ticket(ticket_creator_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have not permissions to interact with this ticket"
        )

    return True


def hide_ticket_body(body: str, result_length: int = 50) -> str:
    return body[:result_length] + ("..." if len(body) >= result_length else "")
