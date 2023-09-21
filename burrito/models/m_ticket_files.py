
from burrito.models.m_basic_model import MongoBaseModel


class TicketFiles(MongoBaseModel):
    ticket_id: int
    file_id: str

    class Meta:
        table_name: str = "ticket_files"
