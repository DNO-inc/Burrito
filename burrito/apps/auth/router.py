from fastapi import APIRouter

from .views import (
    auth__password_login,
    auth__key_login,
    auth__token_refresh,
    auth_delete_refresh_token,
    auth__logout
)


auth_router = APIRouter()

# password auth
auth_router.add_api_route(
    "/password/login",
    auth__password_login,
    methods=["POST"]
)

# key auth
auth_router.add_api_route(
    "/key/login",
    auth__key_login,
    methods=["POST"]
)

# token auth
auth_router.add_api_route(
    "/token/refresh",
    auth__token_refresh,
    methods=["POST"]
)

auth_router.add_api_route(
    "/token/delete",
    auth_delete_refresh_token,
    methods=["POST"]
)

auth_router.add_api_route(
    "/cabinet_logout",
    auth__logout,
    methods=["GET"]
)
