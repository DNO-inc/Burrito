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
    creator: str | None
    hidden: bool | None
    anonymous: bool | None
    faculty_id: str | None
    queue_id: str | None
    status_id: str | None


class TicketIDValue(BaseModel):
    ticket_id: int


class TicketAuthorInfo(BaseModel):
    firstname: str | None
    lastname: str | None
    login: str
    faculty: str | None
    group: str | None
    role: str | None


class TicketDetailInfo(BaseModel):
    creator: TicketAuthorInfo
    assignee: TicketAuthorInfo | None

    ticket_id: int
    subject: str
    body: str
    faculty: str
    status: str
#    actions: list[object]


class TicketListResponse(BaseModel):
    ticket_list: list[TicketDetailInfo]
