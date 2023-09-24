from pydantic import BaseModel

from burrito.models.m_notifications_model import Notifications
from burrito.schemas.comment_schema import CommentDetailInfoScheme


class WebSocketMessage(BaseModel):
    type_: str
    data: Notifications | CommentDetailInfoScheme
