from fastapi import HTTPException, status

from playhouse.shortcuts import model_to_dict

from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users

from burrito.schemas.tickets_schema import TicketUsersInfoSchema
from burrito.schemas.faculty_schema import FacultyResponseSchema


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


def hide_ticket_body(body: str, result_length: int = 500) -> str:
    return body[:result_length] + ("..." if len(body) >= result_length else "")


def make_short_user_data(
    user: Users,
    *,
    hide_user_id: bool = True
) -> TicketUsersInfoSchema:
    user_dict_data = model_to_dict(user)
    user_dict_data["faculty"] = FacultyResponseSchema(
        **model_to_dict(user.faculty)
    )
    if hide_user_id:
        user_dict_data["user_id"] = None

    return TicketUsersInfoSchema(**user_dict_data)
