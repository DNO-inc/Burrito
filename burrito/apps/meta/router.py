from fastapi import APIRouter

from .views import (
    GetStatusesListView,
    GetGroupsListView,
    GetFacultiesListView,
    GetQueuesListView
)


meta_router = APIRouter()

meta_router.add_api_route(
    "/get_statuses",
    GetStatusesListView.get,
    methods=["GET"]
)

meta_router.add_api_route(
    "/get_groups",
    GetGroupsListView.get,
    methods=["GET"]
)

meta_router.add_api_route(
    "/get_faculties",
    GetFacultiesListView.get,
    methods=["GET"]
)

meta_router.add_api_route(
    "/get_queues",
    GetQueuesListView.post,
    methods=["POST"]
)
