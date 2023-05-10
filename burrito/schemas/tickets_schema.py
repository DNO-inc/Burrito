from pydantic import BaseModel


class CreateTicketSchema(BaseModel):
    creator_id: int
    subject: str
    body: str
    hidden: bool
    anonymous: bool
    queue_id: int | bool
    faculty_id: int


class UpdateTicketSchema(BaseModel):
    ticket_id: int
    subject: str | None
    body: str | None
    hidden: bool | None
    anonymous: bool | None


class TicketListRequestSchema(BaseModel):
    creator: str | None
    hidden: bool | None
    anonymous: bool | None
    faculty_id: str | None
    queue_id: str | None
    status_id: str | None


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
    creator: TicketUsersInfoSchema
    assignee: TicketUsersInfoSchema | None

    ticket_id: int
    subject: str
    body: str
    faculty: str
    status: str
#    actions: list[object]


class TicketListResponseSchema(BaseModel):
    ticket_list: list[TicketDetailInfoSchema]
