from pydantic import BaseModel

from burrito.schemas.tickets_schema import TicketUsersInfoSchema


class ActionSchema(BaseModel):
    ticket_id: int
    author: TicketUsersInfoSchema | None
    creation_date: str
    field_name: str
    old_value: str
    new_value: str
    type_: str = "action"


class FileActionSchema(BaseModel):
    ticket_id: int
    author: TicketUsersInfoSchema | None
    creation_date: str
    field_name: str = "file"
    value: str
    type_: str = "action"
