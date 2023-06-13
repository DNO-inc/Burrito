from pydantic import BaseModel

from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
from burrito.schemas.pagination_schema import BurritoPagination
from burrito.schemas.queue_schema import QueueResponseSchema

class AnonTicketListRequestSchema(BurritoPagination):
    anonymous: bool | None
    faculty: str | None
    queue: str | None
    status: list[str] | None


class AnonTicketUsersInfoSchema(BaseModel):
    user_id: int | None
    firstname: str | None
    lastname: str | None
    login: str
    faculty: FacultyResponseSchema
#    role: str | None


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
#    actions: list[object]


class AnonTicketListResponseSchema(BaseModel):
    ticket_list: list[AnonTicketDetailInfoSchema]
    total_pages: int
