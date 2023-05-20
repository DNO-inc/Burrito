from fastapi import APIRouter

from .views import (
    meta__get_statuses_list,
    meta__get_groups_list,
    meta__faculties_list,
    meta__get_queues_list
)


meta_router = APIRouter()

meta_router.add_api_route(
    "/get_statuses",
    meta__get_statuses_list,
    methods=["GET"]
)

meta_router.add_api_route(
    "/get_groups",
    meta__get_groups_list,
    methods=["GET"]
)

meta_router.add_api_route(
    "/get_faculties",
    meta__faculties_list,
    methods=["GET"]
)

meta_router.add_api_route(
    "/get_queues",
    meta__get_queues_list,
    methods=["POST"]
)
