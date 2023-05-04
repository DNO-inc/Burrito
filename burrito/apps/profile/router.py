from fastapi import APIRouter

from burrito.schemas.profile_schema import ProfileSchema

from .views import (
    MyProfileView,
    UpdateMyProfile
)

profile_router = APIRouter()

profile_router.add_api_route(
    "/",
    MyProfileView.post,
    methods=["POST"],
    response_model=ProfileSchema
)
profile_router.add_api_route(
    "/update",
    UpdateMyProfile.post,
    methods=["POST"]
)
