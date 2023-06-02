from pydantic import BaseModel

from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.group_schema import GroupResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
from burrito.schemas.queue_schema import QueueResponseSchema


class AdminUpdateTicketSchema(BaseModel):
    ticket_id: int
    faculty: str | None
    queue: str | None
    status: str | None


class AdminGetTicketListSchema(BaseModel):
    hidden: bool | None
    anonymous: bool | None
    faculty: str | None
    queue: str | None
    status: str | None


class AdminTicketAuthorInfo(BaseModel):
    user_id: int
    firstname: str | None
    lastname: str | None
    login: str
    faculty: FacultyResponseSchema
    group: GroupResponseSchema | None


class AdminTicketDetailInfo(BaseModel):
    creator: AdminTicketAuthorInfo | None
    assignee: AdminTicketAuthorInfo | None

    ticket_id: int
    subject: str
    body: str
    queue: QueueResponseSchema | None
    faculty: FacultyResponseSchema
    status: StatusResponseSchema
    upvotes: int
    is_liked: bool
    date: str


class AdminTicketListResponse(BaseModel):
    ticket_list: list[AdminTicketDetailInfo]


class AdminTicketIdSchema(BaseModel):
    ticket_id: int


class AdminChangePermissionSchema(BaseModel):
    user_id: int
    permission_list: list[str]
    detail: str
