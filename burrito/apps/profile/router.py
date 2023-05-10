from fastapi import APIRouter

from burrito.schemas.profile_schema import ResponseProfileSchema

from .views import (
    MyProfileView,
    UpdateMyProfile
)

profile_router = APIRouter()

profile_router.add_api_route(
    "/",
    MyProfileView.post,
    methods=["POST"],
    response_model=ResponseProfileSchema
)
profile_router.add_api_route(
    "/update",
    UpdateMyProfile.post,
    methods=["POST"]
)
