from fastapi import APIRouter

from .views import (
    admin__update_ticket_data,
    admin__get_ticket_list_by_filter,
    admin__show_detail_ticket_info,
    admin__delete_ticket,
    admin__update_profile
)

admin_router = APIRouter()

admin_router.add_api_route(
    "/profile/update",
    admin__update_profile,
    methods=["PATCH"]
)
admin_router.add_api_route(
    "/tickets/ticket_list",
    admin__get_ticket_list_by_filter,
    methods=["POST"]
)
admin_router.add_api_route(
    "/tickets/{ticket_id}",
    admin__update_ticket_data,
    methods=["PATCH"]
)
admin_router.add_api_route(
    "/tickets/{ticket_id}",
    admin__delete_ticket,
    methods=["DELETE"]
)
admin_router.add_api_route(
    "/tickets/{ticket_id}",
    admin__show_detail_ticket_info,
    methods=["GET"]
)
