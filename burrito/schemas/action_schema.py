from pydantic import BaseModel

from burrito.schemas.tickets_schema import TicketUsersInfoSchema


class ActionSchema(BaseModel):
    action_id: int
    ticket_id: int
    author: TicketUsersInfoSchema | None
    creation_date: str
    field_name: str
    old_value: str
    new_value: str
    type_: str = "action"
