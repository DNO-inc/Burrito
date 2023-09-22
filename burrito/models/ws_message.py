from pydantic import BaseModel

from burrito.models.m_notifications_model import Notifications
from burrito.models.m_comments_model import Comments


class WebSocketMessage(BaseModel):
    type_: str
    data: Notifications | Comments
