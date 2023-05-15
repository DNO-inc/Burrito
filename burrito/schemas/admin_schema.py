from pydantic import BaseModel


class AdminUpdateTicketSchema(BaseModel):
    ticket_id: int
    faculty: str | None
    queue: str | None
    status: str | None


class AdminTicketAuthorInfo(BaseModel):
    firstname: str | None
    lastname: str | None
    login: str
    faculty: str | None
    group: str | None


class AdminGetTicketListSchema(BaseModel):
    hidden: bool | None
    anonymous: bool | None
    faculty: str | None
    queue: str | None
    status: str | None


class AdminTicketDetailInfo(BaseModel):
    creator: AdminTicketAuthorInfo | None
    assignee: AdminTicketAuthorInfo | None

    ticket_id: int
    subject: str
    body: str
    queue: str | None
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
