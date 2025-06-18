from pydantic import BaseModel

from burrito.schemas.division_schema import DivisionResponseSchema
from burrito.schemas.filters_schema import BaseFilterSchema
from burrito.schemas.group_schema import GroupResponseSchema
from burrito.schemas.pagination_schema import BurritoPagination
from burrito.schemas.queue_schema import QueueResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema


class CreateTicketSchema(BaseModel):
    subject: str
    body: str
    hidden: bool
    anonymous: bool
    queue: int
    division: int


class UpdateTicketSchema(BaseModel):
    ticket_id: int
    subject: str | None
    body: str | None
    hidden: bool | None
    anonymous: bool | None


class TicketListRequestSchema(BaseFilterSchema):
    creator: int | None
    assignee: int | None
    hidden: bool | None


class TicketsBasicFilterSchema(BaseFilterSchema):
    hidden: bool | None


class TicketIDValueSchema(BaseModel):
    ticket_id: int


class TicketIDValuesListScheme(BaseModel):
    ticket_id_list: list[int]


class TicketUsersInfoSchema(BaseModel):
    user_id: int | None
    firstname: str | None
    lastname: str | None
    login: str | None
    division: DivisionResponseSchema
    group: GroupResponseSchema | None
#    role: str | None


class TicketDetailInfoSchema(BaseModel):
    creator: TicketUsersInfoSchema | None
    assignee: TicketUsersInfoSchema | None

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


class TicketListResponseSchema(BaseModel):
    ticket_list: list[TicketDetailInfoSchema]
    total_pages: int


class RequestTicketHistorySchema(BurritoPagination):
    ticket_id: int
