from pydantic import BaseModel

from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
from burrito.schemas.group_schema import GroupResponseSchema
from burrito.schemas.pagination_schema import BurritoPagination
from burrito.schemas.queue_schema import QueueResponseSchema

class CreateTicketSchema(BaseModel):
    subject: str
    body: str
    hidden: bool
    anonymous: bool
    queue: int | None
    faculty: str


class UpdateTicketSchema(BaseModel):
    ticket_id: int
    subject: str | None
    body: str | None
    hidden: bool | None
    anonymous: bool | None


class TicketListRequestSchema(BurritoPagination):
    creator: int | None
    hidden: bool | None
    anonymous: bool | None
    faculty: str | None
    queue: str | None
    status: list[str] | None


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
    queue: QueueResponseSchema | None
    status: StatusResponseSchema
    upvotes: int
    is_liked: bool
    is_bookmarked: bool
    date: str
#    actions: list[object]


class TicketListResponseSchema(BaseModel):
    ticket_list: list[TicketDetailInfoSchema]
    total_pages: int
