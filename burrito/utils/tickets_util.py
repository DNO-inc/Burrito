from burrito.models.tickets_model import Tickets


def is_ticket_exist(ticket_id: int) -> Tickets | None:
    """_summary_

    Args:
        ticket_id (int): ticket ID

    Returns:
        Tickets | None: return ticket object if exist else return None
    """

    return Tickets.get_or_none(
        Tickets.ticket_id == ticket_id
    )


def am_i_own_this_ticket(ticket_creator_id: int, user_id: int) -> bool:
    return ticket_creator_id == user_id


def hide_ticket_body(body: str, result_length: int = 50) -> str:
    return body[:result_length] + "..."
