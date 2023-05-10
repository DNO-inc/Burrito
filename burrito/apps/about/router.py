from fastapi import APIRouter

from .views import (
    VersionView, UpdatesView, TeamView
)

about_router = APIRouter()

about_router.add_api_route(
    "/version",
    VersionView.get,
    methods=["GET"]
)
about_router.add_api_route(
    "/updates",
    UpdatesView.get,
    methods=["GET"]
)
about_router.add_api_route(
    "/team",
    TeamView.get,
    methods=["GET"]
)
