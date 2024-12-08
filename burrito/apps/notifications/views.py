from bson.objectid import ObjectId
from fastapi import Depends

from burrito.models.m_notifications_model import NotificationMetaData, Notifications
from burrito.models.user_model import Users
from burrito.utils.auth import get_current_user
from burrito.utils.mongo_util import mongo_delete, mongo_items_count, mongo_select


async def notifications__get_notifications(
    _curr_user: Users = Depends(get_current_user())
):
    notification_list = mongo_select(
        NotificationMetaData,
        start_page=1,
        items_count=500,
        user_id=_curr_user.user_id
    )
    output = mongo_select(
        Notifications,
        start_page=1,
        items_count=500,
        _id={"$in": [ObjectId(i["notification_id"]) for i in notification_list]}
    )

    for item in notification_list:
        mongo_delete(NotificationMetaData, _id=item["_id"])

        if mongo_items_count(
            NotificationMetaData,
            notification_id=item["_id"]
        ) == 0:
            mongo_delete(Notifications, _id=item["notification_id"])

    return {
        "notifications": [Notifications(**i) for i in output]
    }
