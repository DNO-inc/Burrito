from pydantic import BaseModel

from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema


class AnonTicketListRequestSchema(BaseModel):
    anonymous: bool | None
    faculty: str | None
    queue: str | None
    status: str | None


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
    status: StatusResponseSchema
    upvotes: int
    date: str
#    actions: list[object]


class AnonTicketListResponseSchema(BaseModel):
    ticket_list: list[AnonTicketDetailInfoSchema]
