from fastapi import Depends

from burrito.models.m_notifications_model import NotificationMetaData, Notifications

from burrito.utils.mongo_util import mongo_select, mongo_delete, mongo_items_count
from burrito.utils.auth import BurritoJWT, get_auth_core, AuthTokenPayload


async def notifications__get_notifications(__auth_obj: BurritoJWT = Depends(get_auth_core())):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()

    notification_list = mongo_select(NotificationMetaData, user_id=token_payload.user_id)

    for item in notification_list:
        mongo_delete(NotificationMetaData, _id=item["_id"])

        if mongo_items_count(
            NotificationMetaData,
            notification_id=item["_id"]
        ) == 0:
            mongo_delete(Notifications, _id=item["notification_id"])

    return {
        "notifications": notification_list
    }
