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

    if isinstance(raw_data, bytes):
        raw_data = raw_data.decode("utf-8")

    if not raw_data:
        send_data(websocket, b"Auth fail")

    token_payload: AuthTokenPayload = None
    try:
        token_payload = check_jwt_token(raw_data)

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
        server_host = get_config().BURRITO_WEBSOCKET_HOST
        server_port = int(get_config().BURRITO_WEBSOCKET_PORT)
        with serve(
            main_handler,
            server_host,
            server_port,
            logger=get_logger()
        ) as server:
            get_logger().info(f"websocket server running on {server_host}:{server_port}")
            server.serve_forever()

    except Exception as exc:
        get_logger().critical(f"{exc}")
