from pydantic import BaseModel

from burrito.schemas.division_schema import DivisionResponseSchema
from burrito.schemas.filters_schema import BaseFilterSchema
from burrito.schemas.group_schema import GroupResponseSchema
from burrito.schemas.queue_schema import QueueResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema


class AdminUpdateTicketSchema(BaseModel):
    ticket_id: int
    assignee_id: int | None
    division_id: int | None
    queue_id: int | None
    status: int | None


class AdminGetTicketListSchema(BaseFilterSchema):
    creator: int | None
    assignee: int | None
    hidden: bool | None


class AdminTicketAuthorInfo(BaseModel):
    user_id: int
    firstname: str | None
    lastname: str | None
    login: str
    division: DivisionResponseSchema
    group: GroupResponseSchema | None


class AdminTicketDetailInfo(BaseModel):
    creator: AdminTicketAuthorInfo | None
    assignee: AdminTicketAuthorInfo | None

    ticket_id: int
    subject: str
    body: str
    hidden: bool
    anonymous: bool
    division: DivisionResponseSchema
    queue: QueueResponseSchema | None
    status: StatusResponseSchema
    upvotes: int
    is_liked: bool
    is_followed: bool
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
