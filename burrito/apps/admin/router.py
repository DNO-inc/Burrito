from fastapi import APIRouter

from .views import (
    admin__update_ticket_data,
    admin__get_ticket_list_by_filter,
    admin__show_detail_ticket_info,
    admin__delete_ticket,
    admin__update_profile,
    admin__get_followed_tickets
)

admin_router = APIRouter()

admin_router.add_api_route(
    "/tickets/update",
    admin__update_ticket_data,
    methods=["POST"]
)
admin_router.add_api_route(
    "/tickets/ticket_list",
    admin__get_ticket_list_by_filter,
    methods=["POST"]
)
admin_router.add_api_route(
    "/tickets/show",
    admin__show_detail_ticket_info,
    methods=["POST"]
)
admin_router.add_api_route(
    "/tickets/delete",
    admin__delete_ticket,
    methods=["DELETE"]
)
admin_router.add_api_route(
    "/tickets/followed",
    admin__get_followed_tickets,
    methods=["POST"]
)

admin_router.add_api_route(
    "/profile/update",
    admin__update_profile,
    methods=["POST"]
)
