from fastapi import APIRouter

from burrito.schemas.profile_schema import ResponseProfileSchema

from .views import (
    MyProfileView,
    ProfileByPathView,
    UpdateMyProfile
)

profile_router = APIRouter()


profile_router.add_api_route(
    "/",
    MyProfileView.get,
    methods=["GET"],
    response_model=ResponseProfileSchema
)
profile_router.add_api_route(
    "/{user_id}",
    ProfileByPathView.get,
    methods=["GET"],
    response_model=ResponseProfileSchema
)
profile_router.add_api_route(
    "/update",
    UpdateMyProfile.post,
    methods=["POST"]
)
