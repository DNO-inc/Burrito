import datetime

from pydantic import Field

from burrito.models.m_basic_model import MongoBaseModel


class Comments(MongoBaseModel):
    reply_to: int | None
    ticket_id: int
    author_id: int
    creation_date: str = Field(default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    body: str
    type_: str = "comment"

    class Meta:
        table_name: str = "ticket_history"
        history_type: str = "comment"
