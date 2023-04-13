from fastapi import APIRouter

from burrito.apps.about.views import about_index

about_router = APIRouter()

about_router.add_api_route("/", about_index, methods=["get"])
