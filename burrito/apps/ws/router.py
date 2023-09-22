from fastapi import APIRouter

from burrito.apps.ws.views import ws__main


ws_router = APIRouter()

ws_router.add_api_websocket_route("", ws__main)
