from fastapi import APIRouter

from .views import (
    about__get_current_version,
    about__get_changelog_info,
    about__get_info_about_team
)

about_router = APIRouter()

about_router.add_api_route(
    "/version",
    about__get_current_version,
    methods=["GET"]
)
about_router.add_api_route(
    "/updates",
    about__get_changelog_info,
    methods=["GET"]
)
about_router.add_api_route(
    "/team",
    about__get_info_about_team,
    methods=["GET"]
)
