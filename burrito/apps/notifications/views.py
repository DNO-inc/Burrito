from fastapi import Depends

from burrito.models.user_model import Users
from burrito.utils.mongo_util import get_mongo_cursor
from burrito.utils.auth import BurritoJWT, get_auth_core, AuthTokenPayload


async def notifications__get_notifications(__auth_obj: BurritoJWT = Depends(get_auth_core())):
    token_payload: AuthTokenPayload = await __auth_obj.verify_access_token()

    notification_list = get_mongo_cursor()["burrito"]["notifications"].find(
        {
            "user_id": token_payload.user_id
        }
    )

    for n in notification_list:
        print(n)
