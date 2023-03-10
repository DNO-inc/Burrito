from fastapi import APIRouter

from .views import about_index

about_router = APIRouter()

about_router.add_api_route("/", about_index, methods=["get"])
