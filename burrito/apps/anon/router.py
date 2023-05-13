from fastapi import APIRouter

from .views import AnonTicketListView


anon_router = APIRouter()

anon_router.add_api_route(
    "/ticket_list",
    AnonTicketListView.post,
    methods=["POST"]
)
