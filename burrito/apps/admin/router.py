from fastapi import APIRouter

from .views import (
    AdminUpdateTicketsView,
    AdminGetTicketListView,
    AdminTicketDetailInfoView,
    AdminDeleteTicketView,
    AdminChangePermissionsView,
    AdminBecomeAssigneeView
)

admin_router = APIRouter()

admin_router.add_api_route(
    "/tickets/update",
    AdminUpdateTicketsView.post,
    methods=["POST"]
)
admin_router.add_api_route(
    "/tickets/ticket_list",
    AdminGetTicketListView.post,
    methods=["POST"]
)
admin_router.add_api_route(
    "/tickets/show",
    AdminTicketDetailInfoView.post,
    methods=["POST"]
)
admin_router.add_api_route(
    "/tickets/delete",
    AdminDeleteTicketView.post,
    methods=["DELETE"]
)
admin_router.add_api_route(
    "/users/change_permissions",
    AdminChangePermissionsView.post,
    methods=["DELETE"]
)
admin_router.add_api_route(
    "/tickets/become_assignee",
    AdminBecomeAssigneeView.post,
    methods=["POST"]
)
