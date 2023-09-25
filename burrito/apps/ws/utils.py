import time

from redis.client import PubSub
from websockets.sync.server import serve
from websockets.legacy.server import WebSocketServerProtocol

from burrito.utils.config_reader import get_config
from burrito.utils.logger import get_logger
from burrito.utils.auth import check_jwt_token
from burrito.utils.redis_utils import get_redis_connector
from burrito.utils.auth import AuthTokenPayload


def recv_data(websocket: WebSocketServerProtocol) -> bytes:
    try:
        return websocket.recv()
    except:
        ...


def send_data(websocket: WebSocketServerProtocol, data: bytes) -> None:
    try:
        websocket.send(data)
    except:
        ...


def close_conn(websocket: WebSocketServerProtocol) -> None:
    try:
        return websocket.close()
    except:
        ...


def main_handler(websocket: WebSocketServerProtocol):
    raw_data = recv_data(websocket)
    token_payload: AuthTokenPayload = raw_data.decode("utf-8") if raw_data else None

    if not token_payload:
        send_data(websocket, b"Auth fail")

    try:
        token_payload = check_jwt_token(token_payload)

    except:
        send_data(websocket, b"Auth fail")
        close_conn(websocket)
        return

    send_data(websocket, b"Auth OK")

    pubsub: PubSub = get_redis_connector().pubsub()
    pubsub.subscribe(f"user_{token_payload.user_id}")

    try:
        while True:
            message = pubsub.get_message()

            if message:
                data = message.get("data")

                if isinstance(data, bytes):
                    send_data(websocket, data)

            time.sleep(0.5)

    except Exception as exc:
        get_logger().warning(f"{exc}")


def run_websocket_server():
    try:
        with serve(
            main_handler,
            get_config().BURRITO_WEBSOCKET_HOST,
            int(get_config().BURRITO_WEBSOCKET_PORT)
        ) as server:
            server.serve_forever()
    except:
        ...
