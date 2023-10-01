import time
import threading

from redis.client import PubSub
from websockets.sync.server import serve
from websockets.legacy.server import WebSocketServerProtocol

from burrito.utils.config_reader import get_config
from burrito.utils.logger import get_logger
from burrito.utils.auth import check_jwt_token
from burrito.utils.redis_utils import get_redis_connector
from burrito.utils.auth import AuthTokenPayload


def recv_data(websocket: WebSocketServerProtocol) -> bytes:
    return websocket.recv()


def send_data(websocket: WebSocketServerProtocol, data: bytes) -> None:
    websocket.send(data)


def close_conn(websocket: WebSocketServerProtocol) -> None:
    websocket.close()


def recv_ping(websocket: WebSocketServerProtocol) -> None:
    thread_id = threading.get_native_id()
    get_logger().info(f"New pinging thread started: {thread_id}")
    while True:
        try:
            raw_data = recv_data(websocket)

            if isinstance(raw_data, bytes):
                raw_data = raw_data.decode("utf-8")

            if raw_data == "PING":
                send_data(websocket, b"PONG")
                get_logger().info("PING/PONG")

        except Exception as exc:
            get_logger().warning(f"PING/PONG {exc}")
            break

        time.sleep(5)
    get_logger().info(f"Pinging thread is finished {thread_id}")


def notifications_cycle(websocket: WebSocketServerProtocol, token_payload: AuthTokenPayload):
    pubsub: PubSub = get_redis_connector().pubsub()
    pubsub.subscribe(f"user_{token_payload.user_id}")

    pinging_thread = threading.Thread(target=recv_ping, args=(websocket,), daemon=True)
    pinging_thread.start()

    try:
        while True:
            if not pinging_thread.is_alive():
                break

            message = pubsub.get_message()

            if message:
                data = message.get("data")

                if isinstance(data, bytes):
                    send_data(websocket, data)

            time.sleep(0.5)

    except Exception as exc:
        get_logger().warning(f"{exc}")


def chat_cycle(websocket: WebSocketServerProtocol, token_payload: AuthTokenPayload):
    ...


__CONNECTION_MODES = {
    "NOTIFICATIONS": notifications_cycle,
    "CHAT": chat_cycle
}


def main_handler(websocket: WebSocketServerProtocol):
    thread_id = threading.get_native_id()
    get_logger().info(f"New thread started: {thread_id}")

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

    connection_mode = recv_data(websocket)
    if isinstance(connection_mode, bytes):
        connection_mode = connection_mode.decode("utf-8")
    if not connection_mode:
        send_data(websocket, b"Connection mode is invalid")

    connection_handler = __CONNECTION_MODES.get(connection_mode)
    if connection_handler:
        connection_handler(websocket, token_payload)
    else:
        send_data(websocket, b"Connection mode is invalid")
        get_logger().warning(f"User {token_payload.user_id} has selected wrong connection mode '{connection_mode}'")

    get_logger().info(f"Thread {thread_id} is finished")


def run_websocket_server():
    try:
        server_host = get_config().BURRITO_WEBSOCKET_HOST
        server_port = int(get_config().BURRITO_WEBSOCKET_PORT)
        with serve(
            main_handler,
            server_host,
            server_port
        ) as server:
            get_logger().info(f"websocket server running on {server_host}:{server_port}")
            server.serve_forever()

    except Exception as exc:
        get_logger().critical(f"{exc}")
