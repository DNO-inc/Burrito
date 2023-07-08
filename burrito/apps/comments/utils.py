from playhouse.shortcuts import model_to_dict

from fastapi import HTTPException

from burrito.models.user_model import Users
from burrito.models.comments_model import Comments

from burrito.schemas.comment_schema import CommentAuthorInfoSchema
from burrito.schemas.faculty_schema import FacultyResponseSchema


def is_comment_exist_with_error(comment_id: int) -> Comments | None:
    comment: Comments | None = Comments.get_or_none(
        Comments.comment_id == comment_id
    )
    if not comment:
        raise HTTPException(
            status_code=404,
            detail=f"Comment with comment_id {comment.comment_id} is not exists"
        )

    return comment


def is_allowed_to_interact(comment: Comments, user_id: int) -> bool | None:
    if comment.author.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You have not permissions to interact with this comment"
        )
    return True


def make_short_comment_author_info(
        user: Users,
        *,
        hide_user_id: bool = True
) -> CommentAuthorInfoSchema:
    user_dict_data = model_to_dict(user)
    user_dict_data["faculty"] = FacultyResponseSchema(
        **model_to_dict(user.faculty)
    )

    if hide_user_id:
        user_dict_data["user_id"] = None
        user_dict_data["group"] = None
        user_dict_data["firstname"] = None
        user_dict_data["lastname"] = None
        user_dict_data["login"] = None

    return CommentAuthorInfoSchema(**user_dict_data)
