import datetime

from pydantic import Field

from burrito.models.m_basic_model import MongoBaseModel


class Actions(MongoBaseModel):
    ticket_id: int
    user_id: int
    creation_date: str | object = Field(default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    field_name: str = Field(max_length=255)
    old_value: str = Field(max_length=255)
    new_value: str = Field(max_length=255)
    type_: str = "action"

    class Meta:
        table_name: str = "ticket_history"
        history_type: str = "action"
