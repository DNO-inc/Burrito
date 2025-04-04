from pydantic import BaseModel

from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.filters_schema import BaseFilterSchema
from burrito.schemas.queue_schema import QueueResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema


class AnonTicketListRequestSchema(BaseFilterSchema):
    ...


class AnonTicketUsersInfoSchema(BaseModel):
    user_id: int | None
    firstname: str | None
    lastname: str | None
    login: str | None
    faculty: FacultyResponseSchema


class AnonTicketDetailInfoSchema(BaseModel):
    creator: AnonTicketUsersInfoSchema | None
    assignee: AnonTicketUsersInfoSchema | None

    ticket_id: int
    subject: str
    body: str
    faculty: FacultyResponseSchema
    queue: QueueResponseSchema | None
    status: StatusResponseSchema
    upvotes: int
    date: str


class AnonTicketListResponseSchema(BaseModel):
    ticket_list: list[AnonTicketDetailInfoSchema]
    total_pages: int
