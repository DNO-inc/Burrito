from pydantic import BaseModel

from burrito.schemas.pagination_schema import BurritoPagination
from burrito.schemas.tickets_schema import TicketUsersInfoSchema


class CommentCreationSchema(BaseModel):
    reply_to: int | None = None
    ticket_id: int
    body: str


class CommentEditSchema(BaseModel):
    comment_id: int
    body: str | None = ""


class CommentDeletionSchema(BaseModel):
    comment_id: int


class CommentBaseDetailInfoSchema(BaseModel):
    comment_id: int
    author: TicketUsersInfoSchema | None
    body: str

    creation_date: str
    type_: str = "comment"


class CommentDetailInfoScheme(CommentBaseDetailInfoSchema):
    reply_to: CommentBaseDetailInfoSchema | None


class RequestTicketsCommentSchema(BurritoPagination):
    ticket_id: int


class ResponseTicketsCommentSchema(BaseModel):
    ticket_id: int
    comment_list: list[CommentDetailInfoScheme]
