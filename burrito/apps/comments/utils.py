from fastapi.responses import JSONResponse

from burrito.models.comments_model import Comments


def is_comment_exist_with_ext(comment_id: int) -> Comments | None:
    comment: Comments | None = Comments.get_or_none(
        Comments.comment_id == comment_id
    )
    if not comment:
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"Comment with comment_id {comment.comment_id} is not exists"
            }
        )
    return comment


def is_my_comment_with_ext(comment: Comments, user_id: int) -> bool | None:
    if comment.author.user_id != user_id:
        return JSONResponse(
            status_code=403,
            content={
                "detail": "You have not permissions to interact with this comment"
            }
        )
    return True
