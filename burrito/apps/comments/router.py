from fastapi import APIRouter

from .views import (
    comments__create,
    comments__edit,
    comments__delete,
    comments__get_comment_by_id
)


comments_router = APIRouter()

comments_router.add_api_route(
    "/",
    comments__create,
    methods=["POST"]
)
comments_router.add_api_route(
    "/",
    comments__edit,
    methods=["PATCH"]
)
comments_router.add_api_route(
    "/",
    comments__delete,
    methods=["DELETE"]
)
comments_router.add_api_route(
    "/{comment_id}",
    comments__get_comment_by_id,
    methods=["GET"]
)
