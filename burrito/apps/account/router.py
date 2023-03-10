from fastapi import APIRouter

from burrito.apps.account.views import my_account_check

account_router = APIRouter()

account_router.add_api_route("/", my_account_check, methods=["POST"])
