from fastapi import APIRouter

from .views import user_registration

registration_router = APIRouter()

registration_router.add_api_route(
    "/",
    user_registration,
    methods=["POST"]
)
