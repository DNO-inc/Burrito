
from burrito.models.m_basic_model import MongoBaseModel


# TODO: delete field body_ua, instead change body type to dict
class Notifications(MongoBaseModel):
    ticket_id: int
    user_id: int
    body_ua: str
    body: str

    class Meta:
        table_name: str = "notifications"


class NotificationMetaData(MongoBaseModel):
    user_id: int
    notification_id: str

    class Meta:
        table_name = "notification_meta_data"
