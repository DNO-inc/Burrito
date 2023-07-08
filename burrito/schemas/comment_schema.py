from pydantic import BaseModel

from burrito.schemas.pagination_schema import BurritoPagination
from burrito.schemas.group_schema import GroupResponseSchema
from burrito.schemas.faculty_schema import FacultyResponseSchema


class CommentCreationSchema(BaseModel):
    reply_to: int | None = None
    ticket_id: int
    body: str


class CommentEditSchema(BaseModel):
    comment_id: int
    body: str | None


class CommentDeletionSchema(BaseModel):
    comment_id: int


class CommentAuthorInfoSchema(BaseModel):
    user_id: int | None
    firstname: str | None
    lastname: str | None
    login: str | None
    faculty: FacultyResponseSchema
    group: GroupResponseSchema | None


class CommentDetailInfoScheme(BaseModel):
    comment_id: int
    author: CommentAuthorInfoSchema | None
    body: str

    comment_date: str


class RequestTicketsCommentSchema(BurritoPagination):
    ticket_id: int


class ResponseTicketsCommentSchema(BaseModel):
    ticket_id: int
    comment_list: list[CommentDetailInfoScheme]
