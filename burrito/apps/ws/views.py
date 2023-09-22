import asyncio

from starlette.websockets import WebSocket, WebSocketDisconnect
from redis.client import PubSub

from burrito.utils.websockets import _WEBSOCKET_MANAGER
from burrito.utils.logger import get_logger
from burrito.utils.auth import AuthTokenPayload
from burrito.utils.redis_utils import get_redis_connector


async def ws__main(websocket: WebSocket):
    await _WEBSOCKET_MANAGER.accept(websocket)

    token_payload: AuthTokenPayload = await _WEBSOCKET_MANAGER.check_token(websocket)
    if not token_payload:
        return
    await _WEBSOCKET_MANAGER.send(websocket, b"Auth OK")

    pubsub: PubSub = get_redis_connector().pubsub()
    pubsub.subscribe(f"user_{token_payload.user_id}")

    try:
        while True:
            message = pubsub.get_message()

            if message:
                data = message.get("data")

                if isinstance(data, bytes):
                    await _WEBSOCKET_MANAGER.send(websocket, data)

            await asyncio.sleep(0.5)

    except WebSocketDisconnect:
        ...

    except Exception as exc:
        get_logger().warning(f"{exc}")
