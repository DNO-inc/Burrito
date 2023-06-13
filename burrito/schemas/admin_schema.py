from pydantic import BaseModel

from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.group_schema import GroupResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
from burrito.schemas.queue_schema import QueueResponseSchema
from burrito.schemas.pagination_schema import BurritoPagination


class AdminUpdateTicketSchema(BaseModel):
    ticket_id: int
    faculty: str | None
    queue: str | None
    status: str | None


class AdminGetTicketListSchema(BurritoPagination):
    hidden: bool | None
    anonymous: bool | None
    faculty: str | None
    queue: str | None
    status: list[str] | None


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
    faculty: FacultyResponseSchema
    queue: QueueResponseSchema | None
    status: StatusResponseSchema
    upvotes: int
    is_liked: bool
    is_bookmarked: bool
    date: str


class AdminTicketListResponse(BaseModel):
    ticket_list: list[AdminTicketDetailInfo]
    total_pages: int


class AdminTicketIdSchema(BaseModel):
    ticket_id: int


class AdminChangePermissionSchema(BaseModel):
    user_id: int
    permission_list: list[str]
    detail: str
