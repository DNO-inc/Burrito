from pydantic import BaseModel


class CreateTicket(BaseModel):
    creator_id: int
    subject: str
    body: str
    hidden: bool
    anonymous: bool
    queue_id: int | bool
    faculty_id: int


class UpdateTicket(BaseModel):
    ticket_id: int
    subject: str | None
    body: str | None
    hidden: bool | None
    anonymous: bool | None


class TicketList(BaseModel):
    issuer: str | None
    hidden: bool | None
    anonymous: bool | None
    faculty: str | None
    tag: str | None
    status: str | None


class TicketIDValue(BaseModel):
    ticket_id: int
