from fastapi import APIRouter

from burrito.apps.auth.views import password_login, token_login


auth_router = APIRouter()

# password auth
auth_router.add_api_route("/password/login", password_login, methods=["POST"])

# token auth
auth_router.add_api_route("/token/login", token_login, methods=["POST"])
# auth_router.add_api_route("/token/logout", token_login, methods=["POST"])
# auth_router.add_api_route("/token/refresh", token_login, methods=["POST"])
