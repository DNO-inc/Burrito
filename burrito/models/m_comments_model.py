from pydantic import Field

from burrito.models.m_basic_model import MongoBaseModel
from burrito.utils.date import get_datetime_now


class Comments(MongoBaseModel):
    reply_to: str | None
    ticket_id: int
    author_id: int
    creation_date: str = Field(default_factory=get_datetime_now)
    body: str
    type_: str = "comment"

    class Meta:
        table_name: str = "ticket_history"
        history_type: str = "comment"
