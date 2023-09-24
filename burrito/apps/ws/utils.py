import asyncio

from redis.client import PubSub
from websockets.server import serve
from websockets.legacy.server import WebSocketServerProtocol

from burrito.utils.config_reader import get_config
from burrito.utils.logger import get_logger
from burrito.utils.auth import check_jwt_token
from burrito.utils.redis_utils import get_redis_connector
from burrito.utils.auth import AuthTokenPayload


async def recv_data(websocket: WebSocketServerProtocol) -> bytes:
    try:
        return await websocket.recv()
    except:
        ...


async def send_data(websocket: WebSocketServerProtocol, data: bytes) -> None:
    try:
        await websocket.send(data)
    except:
        ...


async def close_conn(websocket: WebSocketServerProtocol) -> None:
    try:
        return await websocket.close()
    except:
        ...


async def main_handler(websocket: WebSocketServerProtocol):
    raw_data = await recv_data(websocket)
    token_payload: AuthTokenPayload = raw_data.decode("utf-8") if raw_data else None

    if not token_payload:
        await send_data(websocket, b"Auth fail")

    try:
        token_payload = await check_jwt_token(token_payload)

    except:
        await send_data(websocket, b"Auth fail")
        await close_conn(websocket)
        return

    await send_data(websocket, b"Auth OK")

    pubsub: PubSub = get_redis_connector().pubsub()
    pubsub.subscribe(f"user_{token_payload.user_id}")

    try:
        while True:
            message = pubsub.get_message()

            if message:
                data = message.get("data")

                if isinstance(data, bytes):
                    await send_data(websocket, data)

            await asyncio.sleep(0.5)

    except Exception as exc:
        get_logger().warning(f"{exc}")


ws_server = serve(
    main_handler,
    get_config().BURRITO_WEBSOCKET_HOST,
    int(get_config().BURRITO_WEBSOCKET_PORT)
)


def run_websocket_server():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ws_server)
    loop.run_forever()
