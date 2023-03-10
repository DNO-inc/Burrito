
from fastapi import APIRouter

from .views import password_login, token_login



auth_router = APIRouter()

auth_router.add_api_route("/password/login", password_login, methods=["POST"])
auth_router.add_api_route("/token/login", token_login, methods=["POST"])


