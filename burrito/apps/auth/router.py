from fastapi import APIRouter

from .views import auth__password_login, auth__token_login


auth_router = APIRouter()

# password auth
auth_router.add_api_route(
    "/password/login",
    auth__password_login,
    methods=["POST"]
)

# token auth
auth_router.add_api_route(
    "/token/login",
    auth__token_login,
    methods=["POST"]
)
# auth_router.add_api_route("/token/logout", token_login, methods=["POST"])
# auth_router.add_api_route("/token/refresh", token_login, methods=["POST"])
