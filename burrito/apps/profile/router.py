from fastapi import APIRouter

from .views import (
    profile__check_by_id,
    profile__get_new_token,
    profile__token_reset_request,
    profile__update_my_profile,
)
from burrito.schemas.profile_schema import ResponseProfileSchema

profile_router = APIRouter()


profile_router.add_api_route(
    "/update",
    profile__update_my_profile,
    methods=["POST"]
)
profile_router.add_api_route(
    "/access_renew/{reset_token}",
    profile__get_new_token,
    methods=["GET"]
)
profile_router.add_api_route(
    "/access_renew",
    profile__token_reset_request,
    methods=["GET"],
    name="access_renew_route"
)
profile_router.add_api_route(
    "/{user_id}",
    profile__check_by_id,
    methods=["GET"],
    response_model=ResponseProfileSchema
)
