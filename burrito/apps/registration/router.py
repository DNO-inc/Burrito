from fastapi import APIRouter

from .views import (
    registration_main,
    check_verification_code
)

registration_router = APIRouter()

registration_router.add_api_route("/", registration_main, methods=["POST"])
registration_router.add_api_route("/send_code", check_verification_code, methods=["POST"])
