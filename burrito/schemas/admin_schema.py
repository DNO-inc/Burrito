from pydantic import BaseModel


class AdminUpdateTicketSchema(BaseModel):
    ticket_id: int
    faculty_id: int | None
    queue_id: int | None
    status_id: int | None

class AdminTicketAuthorInfo(BaseModel):
    firstname: str | None
    lastname: str | None
    login: str
    faculty: str | None
    group: str | None
    role: str | None


class AdminGetTicketListSchema(BaseModel):
    creator: int | None
    hidden: bool | None
    anonymous: bool | None
    faculty_id: int | None
    queue_id: int | None
    status_id: int | None


class AdminTicketDetailInfo(BaseModel):
    creator: AdminTicketAuthorInfo
    assignee: AdminTicketAuthorInfo | None

    ticket_id: int
    subject: str
    body: str
    faculty: str
    status: str


class AdminTicketListResponse(BaseModel):
    ticket_list: list[AdminTicketDetailInfo]


class AdminTicketIdSchema(BaseModel):
    ticket_id: int


class AdminChangePermissionSchema(BaseModel):
    user_id: int
    permission_list: list[str]
    detail: str
