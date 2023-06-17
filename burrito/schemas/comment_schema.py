from pydantic import BaseModel


class CommentCreationSchema(BaseModel):
    reply_to: int | None = None
    ticket_id: int
    body: str


class CommentEditSchema(BaseModel):
    comment_id: int
    make_upvote: bool | None = None
    body: str | None


class CommentDeletionSchema(BaseModel):
    comment_id: int
