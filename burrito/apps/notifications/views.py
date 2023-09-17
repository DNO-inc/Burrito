from fastapi import Depends

from burrito.models.m_notifications_model import Notifications

from burrito.utils.mongo_util import mongo_select
from burrito.utils.auth import BurritoJWT, get_auth_core, AuthTokenPayload


async def notifications__get_notifications(__auth_obj: BurritoJWT = Depends(get_auth_core())):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()

    notification_list = mongo_select(Notifications, user_id=token_payload.user_id)

    for n in notification_list:
        print(n)
