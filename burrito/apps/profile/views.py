from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse

from burrito.models.m_password_rest_model import AccessRenewMetaData
from burrito.models.user_model import Users
from burrito.schemas.profile_schema import (
    RequestUpdateProfileSchema,
    ResponseProfileSchema,
)
from burrito.utils.auth import (
    AuthTokenPayload,
    create_access_token,
    create_refresh_token,
    get_current_user,
)
from burrito.utils.email_util import load_email_template, publish_email
from burrito.utils.mongo_util import mongo_delete, mongo_insert, mongo_select
from burrito.utils.users_util import get_user_by_email_or_none, get_user_by_id

from .utils import generate_reset_token, update_profile_data, view_profile_by_user_id

# TODO: it should be changed to env variable or we need to come up with another way to receive an actual URI for access renewing
__ACCESS_RENEW_URL_TEMPLATE = "https://tres.sumdu.edu.ua/general_tickets?reset_token={}"


async def profile__check_by_id(
    user_id: int,
    _curr_user: Users = Depends(get_current_user())
) -> ResponseProfileSchema:
    """Return some data to check user profile"""

    return await view_profile_by_user_id(user_id)


async def profile__update_my_profile(
    profile_updated_data: RequestUpdateProfileSchema | None = RequestUpdateProfileSchema(),
    _curr_user: Users = Depends(get_current_user(permission_list={"UPDATE_PROFILE"}))
):
    """Update profile data"""

    await update_profile_data(_curr_user, profile_updated_data)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Profile was updated"}
    )


async def profile__token_reset_request(
    email: str
):
    user_data: Users | None = get_user_by_email_or_none(email)
    if not user_data:
        raise HTTPException(
            status_code=404,
            detail="User is not exists"
        )

    reset_token = generate_reset_token()

    mongo_insert(
        AccessRenewMetaData(
            user_id=user_data.user_id,
            reset_token=reset_token
        )
    )

    publish_email(
        [user_data.user_id],
        "Запит на поновлення доступу до TreS",
        load_email_template(
            "email/access_renew.html",
            {
                "url": __ACCESS_RENEW_URL_TEMPLATE.format(reset_token)
            }
        )
    )

    return {
        "detail": "Please check email to renew access to TreS"
    }


async def profile__get_new_token(
    reset_token: str,
    _curr_user: Users = Depends(get_current_user())
):
    access_renew_metadata = mongo_select(
        AccessRenewMetaData,
        reset_token=reset_token
    )
    if not access_renew_metadata:
        raise HTTPException(
            status_code=404,
            detail="No meta data found"
        )
    mongo_delete(
        AccessRenewMetaData,
        reset_token=reset_token
    )

    access_renew_metadata = access_renew_metadata[0]
    user: Users = get_user_by_id(access_renew_metadata["user_id"])

    payload = AuthTokenPayload(
        user_id=user.user_id,
        role=user.role.name
    )

    return {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload)
    }
