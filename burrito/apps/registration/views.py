from burrito.models.user_model import Users
from burrito.schemas.user_schema import UserPasswordLoginSchema
from burrito.utils.hash_util import get_hash
from burrito.utils.db_utils import create_user, get_user_by_login


async def registration_main(user_data: UserPasswordLoginSchema):
    """Handle user registration"""

    if (get_user_by_login(user_data.login)):
        return {"detail": "User user with the same login exist."}

    user_creation_status = create_user(
        user_data.login,
        get_hash(user_data.password)
    )

    if (user_creation_status):
        return {"code": "successfully"}
    else:
        return {"code": "unsuccessfully"}
