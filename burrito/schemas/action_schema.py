from pydantic import BaseModel

from burrito.schemas.tickets_schema import TicketUsersInfoSchema


class BaseActionSchems(BaseModel):
    ticket_id: int
    author: TicketUsersInfoSchema | None
    creation_date: str
    field_name: str
    type_: str = "action"


class ActionSchema(BaseActionSchems):
    old_value: str
    new_value: str


class FileActionSchema(BaseActionSchems):
    field_name: str = "file"
    value: str
