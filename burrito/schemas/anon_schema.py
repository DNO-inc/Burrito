from pydantic import BaseModel


class AnonTicketListRequestSchema(BaseModel):
    anonymous: bool | None
    faculty: str | None
    queue: str | None
    status: str | None


class AnonTicketUsersInfoSchema(BaseModel):
    firstname: str | None
    lastname: str | None
    login: str
    faculty: str | None
#    role: str | None


class AnonTicketDetailInfoSchema(BaseModel):
    creator: AnonTicketUsersInfoSchema | None
    assignee: AnonTicketUsersInfoSchema | None

    ticket_id: int
    subject: str
    body: str
    faculty: str
    status: str
    upvotes: int
#    actions: list[object]


class AnonTicketListResponseSchema(BaseModel):
    ticket_list: list[AnonTicketDetailInfoSchema]
