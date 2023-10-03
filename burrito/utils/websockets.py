import orjson as json

from burrito.models.ws_message import WebSocketMessage
from burrito.models.m_notifications_model import Notifications


def make_websocket_message(type_: str, obj: Notifications) -> bytes:
    """
    Create a WebSocket message.

    Returns:
        The JSON serialized version of the message as a bytes object.
    """
    return json.dumps(
        WebSocketMessage(
            type_=type_,
            data=obj
        ).dict()
    )
