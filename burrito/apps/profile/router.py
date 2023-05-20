from fastapi import APIRouter

from burrito.schemas.profile_schema import ResponseProfileSchema

from .views import (
    profile__check_my_profile,
    profile__check_by_id,
    profile__update_my_profile
)

profile_router = APIRouter()


profile_router.add_api_route(
    "/",
    profile__check_my_profile,
    methods=["GET"],
    response_model=ResponseProfileSchema
)
profile_router.add_api_route(
    "/{user_id}",
    profile__check_by_id,
    methods=["GET"],
    response_model=ResponseProfileSchema
)
profile_router.add_api_route(
    "/update",
    profile__update_my_profile,
    methods=["POST"]
)
