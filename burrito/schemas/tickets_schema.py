from pydantic import BaseModel


class CreateTicket(BaseModel):
    ...


class DeleteTicket(BaseModel):
    ...


class SaveTicket(BaseModel):
    ...


class FollowTicket(BaseModel):
    ...


class CloseTicket(BaseModel):
    ...
