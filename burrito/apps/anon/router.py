from fastapi import APIRouter

from .views import anon__get_ticket_list_by_filter

anon_router = APIRouter()

anon_router.add_api_route(
    "/ticket_list",
    anon__get_ticket_list_by_filter,
    methods=["POST"]
)
