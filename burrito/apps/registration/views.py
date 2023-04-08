from fastapi.responses import JSONResponse

from burrito.schemas.user_schema import (
    UserPasswordLoginSchema,
    UserVerificationCode
)
from burrito.utils.hash_util import get_hash
from burrito.utils.db_utils import create_user, get_user_by_login

from burrito.utils.validators import is_valid_login, is_valid_password
from burrito.utils.redis_utils import get_redis_cursor

from burrito.utils.email_utils import send_test_email_via_redis


async def registration_main(user_data: UserPasswordLoginSchema):
    """Handle user registration"""

    if not is_valid_login(user_data.login):
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid login"}
        )

    if not is_valid_password(user_data.password):
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid password"}
        )

    if await get_redis_cursor().is_user_exist(user_data.login):
        return {"detail": "User with the same login exist."}

    if get_user_by_login(user_data.login):
        return {"detail": "User with the same login exist."}

    pubsub = get_redis_cursor().pubsub()
    pubsub.subscribe("test_email_messages")

    await send_test_email_via_redis(
        "test_email_messages",
        await get_redis_cursor().put_user_login_data(user_data)
    )

    await pubsub.get_message()

    # TODO: delete from this handler
    user_creation_status = create_user(
        user_data.login,
        get_hash(user_data.password)
    )

    if user_creation_status:
        return {"code": "successfully"}

    return {"code": "unsuccessfully"}


async def check_verification_code(code_object: UserVerificationCode):
    ...
