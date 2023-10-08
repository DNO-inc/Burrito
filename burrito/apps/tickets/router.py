from fastapi import APIRouter

from burrito.apps.tickets.views import (
    tickets__create_new_ticket,
    tickets__delete_ticket_for_me,
    tickets__bookmark_ticket,
    tickets__like_ticket,
    tickets__unlike_ticket,
    tickets__unbookmark_ticket,
    tickets__show_tickets_list_by_filter,
    tickets__show_detail_ticket_info,
    tickets__update_own_ticket_data,
    tickets__close_own_ticket,
    tickets__get_liked_tickets,
    tickets__get_bookmarked_tickets,
    tickets__get_deleted_tickets,
    tickets__undelete_ticket,
    tickets__get_followed_tickets,
    tickets__get_full_ticket_history,
    tickets__get_action_by_id
)


tickets_router = APIRouter()

tickets_router.add_api_route(
    "/create",
    tickets__create_new_ticket,
    methods=["POST"]
)
tickets_router.add_api_route(
    "/update",
    tickets__update_own_ticket_data,
    methods=["POST"]
)
tickets_router.add_api_route(
    "/close",
    tickets__close_own_ticket,
    methods=["POST"]
)

tickets_router.add_api_route(
    "/delete",
    tickets__delete_ticket_for_me,
    methods=["DELETE"]
)
tickets_router.add_api_route(
    "/undelete",
    tickets__undelete_ticket,
    methods=["POST"]
)
tickets_router.add_api_route(
    "/deleted",
    tickets__get_deleted_tickets,
    methods=["POST"]
)

tickets_router.add_api_route(
    "/bookmark",
    tickets__bookmark_ticket,
    methods=["POST"]
)
tickets_router.add_api_route(
    "/unbookmark",
    tickets__unbookmark_ticket,
    methods=["POST"]
)
tickets_router.add_api_route(
    "/bookmarked",
    tickets__get_bookmarked_tickets,
    methods=["POST"]
)
tickets_router.add_api_route(
    "/followed",
    tickets__get_followed_tickets,
    methods=["POST"]
)

tickets_router.add_api_route(
    "/like",
    tickets__like_ticket,
    methods=["POST"]
)
tickets_router.add_api_route(
    "/unlike",
    tickets__unlike_ticket,
    methods=["POST"]
)
tickets_router.add_api_route(
    "/liked",
    tickets__get_liked_tickets,
    methods=["POST"]
)

tickets_router.add_api_route(
    "/ticket_list",
    tickets__show_tickets_list_by_filter,
    methods=["POST"]
)
tickets_router.add_api_route(
    "/show",
    tickets__show_detail_ticket_info,
    methods=["POST"]
)
tickets_router.add_api_route(
    "/full_history",
    tickets__get_full_ticket_history,
    methods=["POST"]
)
tickets_router.add_api_route(
    "/get_action",
    tickets__get_action_by_id,
    methods=["POST"]
)
