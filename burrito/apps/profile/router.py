from fastapi import APIRouter

from burrito.apps.profile.views import my_profile, update_my_profile

profile_router = APIRouter()

profile_router.add_api_route("/", my_profile, methods=["POST"])
profile_router.add_api_route(
    "/update_info",
    update_my_profile,
    methods=["POST"]
)
