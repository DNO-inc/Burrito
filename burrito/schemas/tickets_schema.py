from pydantic import BaseModel

from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
from burrito.schemas.group_schema import GroupResponseSchema


class CreateTicketSchema(BaseModel):
    subject: str
    body: str
    hidden: bool
    anonymous: bool
    queue: str | None
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
    user_id: int | None
    firstname: str | None
    lastname: str | None
    login: str
    faculty: FacultyResponseSchema
    group: GroupResponseSchema | None
#    role: str | None


class TicketDetailInfoSchema(BaseModel):
    creator: TicketUsersInfoSchema | None
    assignee: TicketUsersInfoSchema | None

    ticket_id: int
    subject: str
    body: str
    faculty: FacultyResponseSchema
    status: StatusResponseSchema
    upvotes: int
    is_liked: bool
    is_bookmarked: bool
    date: str
#    actions: list[object]


class TicketListResponseSchema(BaseModel):
    ticket_list: list[TicketDetailInfoSchema]
