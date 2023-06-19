from pydantic import BaseModel


class ActionSchema(BaseModel):
    action_id: int
    ticket_id: int
    author_id: int
    action_date: str
    field_name: str
    old_value: str
    new_value: str
