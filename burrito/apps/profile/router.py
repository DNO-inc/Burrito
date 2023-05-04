from fastapi import APIRouter

from burrito.schemas.profile_schema import ProfileSchema

from .views import my_profile, update_my_profile

profile_router = APIRouter()

profile_router.add_api_route(
    "/",
    my_profile,
    methods=["POST"],
    response_model=ProfileSchema
)
profile_router.add_api_route(
    "/update",
    update_my_profile,
    methods=["POST"]
)
