from fastapi import APIRouter

from .views import registration__user_registration, registration__verify_email

registration_router = APIRouter()

registration_router.add_api_route(
    "/",
    registration__user_registration,
    methods=["POST"]
)

registration_router.add_api_route(
    "/verify_email",
    registration__verify_email,
    methods=["POST"]
)
