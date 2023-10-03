from pydantic import Field

from burrito.utils.date import get_datetime_now
from burrito.models.m_basic_model import MongoBaseModel


class Actions(MongoBaseModel):
    ticket_id: int
    user_id: int
    creation_date: str | object = Field(default_factory=get_datetime_now)
    field_name: str = Field(max_length=255)
    old_value: str = Field(max_length=255)
    new_value: str = Field(max_length=255)
    type_: str = "action"

    class Meta:
        table_name: str = "ticket_history"
        history_type: str = "action"


class FileActions(MongoBaseModel):
    ticket_id: int
    user_id: int
    creation_date: str | object = Field(default_factory=get_datetime_now)
    field_name: str = "file"
    value: str = Field(max_length=255)
    type_: str = "action"

    class Meta:
        table_name: str = "ticket_history"
        history_type: str = "action"
