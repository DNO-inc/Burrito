from fastapi import APIRouter

from .views import RegistrationMainView

registration_router = APIRouter()

registration_router.add_api_route(
    "/",
    RegistrationMainView.post,
    methods=["POST"]
)
