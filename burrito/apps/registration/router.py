from fastapi import APIRouter

from burrito.apps.registration.views import registration_main

registration_router = APIRouter()

registration_router.add_api_route("/", registration_main, methods=["POST"])
