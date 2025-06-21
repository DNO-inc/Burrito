from fastapi import APIRouter

from .views import (
    statistic__activity_summary,
    statistic__divisions,
    statistic__periodic,
)

statistic_router = APIRouter()


statistic_router.add_api_route(
    "/activity_summary",
    statistic__activity_summary,
    methods=["GET"]
)

statistic_router.add_api_route(
    "/divisions",
    statistic__divisions,
    methods=["GET"]
)

statistic_router.add_api_route(
    "/period",
    statistic__periodic,
    methods=["GET"]
)
