from fastapi import APIRouter

from burrito.apps.reports.views import (
    my_reports, to_me,
    followed, create_new_report
)


reports_router = APIRouter()

reports_router.add_api_route("/my", my_reports, methods=["POST"])
reports_router.add_api_route("/to_me", to_me, methods=["POST"])
reports_router.add_api_route("/followed", followed, methods=["POST"])
reports_router.add_api_route("/create", create_new_report, methods=["POST"])
