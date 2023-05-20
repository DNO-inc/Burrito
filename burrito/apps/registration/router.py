from fastapi import APIRouter

from .views import registration__user_registration

registration_router = APIRouter()

registration_router.add_api_route(
    "/",
    registration__user_registration,
    methods=["POST"]
)
