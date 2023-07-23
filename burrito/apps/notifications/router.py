from fastapi import APIRouter

from .views import (
    notifications__get_notifications
)


notifications_router = APIRouter()

notifications_router.add_api_route(
    "/",
    notifications__get_notifications,
    methods=["GET"]
)
