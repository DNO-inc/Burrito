from fastapi import APIRouter

from .views import (
    comments__create,
    comments__edit,
    comments__delete
)


comments_router = APIRouter()

comments_router.add_api_route(
    "/create",
    comments__create,
    methods=["POST"]
)
comments_router.add_api_route(
    "/edit",
    comments__edit,
    methods=["POST"]
)
comments_router.add_api_route(
    "/delete",
    comments__delete,
    methods=["DELETE"]
)
