from pydantic import BaseModel


class CreateTicketSchema(BaseModel):
    subject: str
    body: str
    hidden: bool
    anonymous: bool
    queue: str
    faculty: str


class UpdateTicketSchema(BaseModel):
    ticket_id: int
    subject: str | None
    body: str | None
    hidden: bool | None
    anonymous: bool | None


class TicketListRequestSchema(BaseModel):
    creator: int | None
    hidden: bool | None
    anonymous: bool | None
    faculty: str | None
    queue: str | None
    status: str | None


class TicketIDValueSchema(BaseModel):
    ticket_id: int


class TicketUsersInfoSchema(BaseModel):
    firstname: str | None
    lastname: str | None
    login: str
    faculty: str | None
#    group: str | None
#    role: str | None


class TicketDetailInfoSchema(BaseModel):
    creator: TicketUsersInfoSchema | None
    assignee: TicketUsersInfoSchema | None

    ticket_id: int
    subject: str
    body: str
    faculty: str
    status: str
#    actions: list[object]


class TicketListResponseSchema(BaseModel):
    ticket_list: list[TicketDetailInfoSchema]
