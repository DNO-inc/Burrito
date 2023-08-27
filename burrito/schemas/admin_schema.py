from pydantic import BaseModel

from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.group_schema import GroupResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
from burrito.schemas.queue_schema import QueueResponseSchema
from burrito.schemas.action_schema import ActionSchema
from burrito.schemas.filters_schema import BaseFilterSchema


class AdminUpdateTicketSchema(BaseModel):
    ticket_id: int
    assignee_id: int | None
    faculty: int | None
    queue: int | None
    status: int | None


class AdminGetTicketListSchema(BaseFilterSchema):
    creator: int | None
    assignee: int | None = -1
    hidden: bool | None


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
    history: list[ActionSchema] = []


class AdminTicketListResponse(BaseModel):
    ticket_list: list[AdminTicketDetailInfo]
    total_pages: int


class AdminTicketIdSchema(BaseModel):
    ticket_id: int


class AdminChangePermissionSchema(BaseModel):
    user_id: int
    permission_list: list[str]
    detail: str
