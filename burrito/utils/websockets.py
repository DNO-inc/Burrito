import orjson as json
from starlette.websockets import WebSocket

from burrito.utils.singleton_pattern import singleton
from burrito.utils.auth import check_jwt_token

from burrito.models.ws_message import WebSocketMessage
from burrito.models.m_notifications_model import Notifications
from burrito.schemas.comment_schema import CommentDetailInfoScheme


@singleton
class WebsocketManager:
    def __init__(self) -> None:
        self._websocket_list: list[WebSocket] = []

    async def accept(self, websocket: WebSocket):
        await websocket.accept()
        self._websocket_list.append(websocket)

    async def check_token(self, websocket: WebSocket) -> bool:
        token = (await self.recv(websocket)).decode("utf-8")

        try:
            return await check_jwt_token(token)
        except:
            await self.send(websocket, b"Auth fail")
            await self.close(websocket)

    async def recv(self, websocket: WebSocket) -> bytes:
        return await websocket.receive_bytes()

    async def send(self, websocket: WebSocket, data: bytes):
        await websocket.send_bytes(data)

    async def close(self, websocket: WebSocket):
        self._websocket_list.remove(websocket)
        await websocket.close()


def get_websocket_manager():
    return WebsocketManager()


_WEBSOCKET_MANAGER: WebsocketManager = get_websocket_manager()


def make_websocket_message(type_: str, obj: CommentDetailInfoScheme | Notifications) -> bytes:
    return json.dumps(
        WebSocketMessage(
            type_=type_,
            data=obj
        ).dict()
    )
