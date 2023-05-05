from fastapi import APIRouter

from .views import (
    RegistrationMainView,
    check_verification_code
)

registration_router = APIRouter()

registration_router.add_api_route(
    "/",
    RegistrationMainView.post,
    methods=["POST"]
)
registration_router.add_api_route(
    "/send_code",
    check_verification_code,
    methods=["POST"]
)
