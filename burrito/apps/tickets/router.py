from fastapi import APIRouter

from burrito.apps.tickets.views import (
    CreateTicketView,
    DeleteTicketView,
    BookmarkTicketView,
    TicketListView,
    TicketDetailInfoView,
    UpdateTicketView,
    CloseTicketView
)


tickets_router = APIRouter()

tickets_router.add_api_route(
    "/create",
    CreateTicketView.post,
    methods=["POST"]
)
tickets_router.add_api_route(
    "/delete",
    DeleteTicketView.delete,
    methods=["DELETE"]
)
tickets_router.add_api_route(
    "/bookmark",
    BookmarkTicketView.post,
    methods=["POST"]
)
tickets_router.add_api_route(
    "/ticket_list",
    TicketListView.post,
    methods=["POST"]
)
tickets_router.add_api_route(
    "/show",
    TicketDetailInfoView.post,
    methods=["POST"]
)
tickets_router.add_api_route(
    "/update",
    UpdateTicketView.post,
    methods=["POST"]
)
tickets_router.add_api_route(
    "/close",
    CloseTicketView.post,
    methods=["POST"]
)
