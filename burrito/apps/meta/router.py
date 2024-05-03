from fastapi import APIRouter

from .views import (
    meta__get_statuses_list,
    meta__get_groups_list,
    meta__faculties_list,
    meta__get_queues_list,
    meta__get_admins,
    meta__get_roles,
    meta__get_role_permissions
)


meta_router = APIRouter()

meta_router.add_api_route(
    "/statuses",
    meta__get_statuses_list,
    methods=["GET"]
)

meta_router.add_api_route(
    "/groups",
    meta__get_groups_list,
    methods=["GET"]
)

meta_router.add_api_route(
    "/faculties",
    meta__faculties_list,
    methods=["GET"]
)

meta_router.add_api_route(
    "/queues/by_faculty/{faculty}",
    meta__get_queues_list,
    methods=["GET"]
)

meta_router.add_api_route(
    "/admins",
    meta__get_admins,
    methods=["GET"]
)

meta_router.add_api_route(
    "/roles",
    meta__get_roles,
    methods=["GET"]
)

meta_router.add_api_route(
    "/role_permissions",
    meta__get_role_permissions,
    methods=["GET"]
)
