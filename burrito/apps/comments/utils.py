from bson.objectid import ObjectId
from fastapi import HTTPException

from burrito.models.m_comments_model import Comments
from burrito.utils.mongo_util import mongo_select


def is_comment_exist_with_error(comment_id: str) -> Comments | None:
    comment: Comments | None = mongo_select(Comments, _id=ObjectId(comment_id))
    if comment:
        comment = comment[0]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Comment with comment_id {comment_id} is not exists"
        )

    if not comment.get("type_"):
        raise HTTPException(
            status_code=404,
            detail=f"Comment with comment_id {comment_id} is not exists"
        )

    if comment["type_"] != "comment":
        raise HTTPException(
            status_code=404,
            detail=f"Comment with comment_id {comment_id} is not exists"
        )

    return comment


def is_allowed_to_interact(comment: Comments, user_id: int) -> bool | None:
    if comment["author_id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="You have not permissions to interact with this comment"
        )
    return True
