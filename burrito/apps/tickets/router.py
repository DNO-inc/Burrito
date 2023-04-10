from fastapi import APIRouter

from burrito.apps.tickets.views import (
    my_reports, to_me,
    followed, create_new_report
)


tickets_router = APIRouter()

tickets_router.add_api_route("/my", my_reports, methods=["POST"])
tickets_router.add_api_route("/to_me", to_me, methods=["POST"])
tickets_router.add_api_route("/followed", followed, methods=["POST"])
tickets_router.add_api_route("/create", create_new_report, methods=["POST"])
