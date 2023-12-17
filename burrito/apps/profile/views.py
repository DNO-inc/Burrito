from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse

from burrito.schemas.profile_schema import (
    ResponseProfileSchema,
    RequestUpdateProfileSchema
)
from burrito.models.m_password_rest_model import AccessRenewMetaData
from burrito.models.user_model import Users

from burrito.utils.email_util import publish_email
from burrito.utils.email_templates import TEMPLATE__ACCESS_RENEW_REQUEST_EMAIL
from burrito.utils.mongo_util import mongo_insert, mongo_select, mongo_delete
from burrito.utils.auth import AuthTokenPayload, BurritoJWT
from burrito.utils.users_util import (
    is_admin,
    is_chief_admin,
    get_user_by_email_or_none,
    get_user_by_id
)

from .utils import (
    get_auth_core,
    check_permission,
    view_profile_by_user_id,
    update_profile_data,
    generate_reset_token
)


# TODO: it should be changed to env variable or we need to come up with another way to receive an actual URI for access renewing
__ACCESS_RENEW_URL_TEMPLATE = "https://demo.tres.cyberbydlo.com/general_tickets?reset_token={}"


async def profile__check_by_id(
    user_id: int,
    __auth_obj: BurritoJWT = Depends(get_auth_core())
) -> ResponseProfileSchema:
    """Return some data to check user profile"""

    await __auth_obj.require_access_token()

    return await view_profile_by_user_id(user_id)


async def profile__update_my_profile(
    profile_updated_data: RequestUpdateProfileSchema | None = RequestUpdateProfileSchema(),
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Update profile data"""

    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, permission_list={"UPDATE_PROFILE"})

    target_user_id = -1
    # if token owner is admin we can allow to change profiles of other users
    # otherwise the profile of the token owner will be changed

    _curr_is_admin: bool = is_admin(token_payload.user_id)
    _curr_is_chief_admin: bool = is_chief_admin(token_payload.user_id)

    _target_is_admin: bool = is_admin(profile_updated_data.user_id) if profile_updated_data.user_id else False
    _target_is_chief_admin: bool = is_chief_admin(profile_updated_data.user_id) if profile_updated_data.user_id else False
    # CHIEF_ADMIN is able to change every bodies profiles
    if profile_updated_data.user_id and _curr_is_chief_admin:
        target_user_id = profile_updated_data.user_id
    elif (
        profile_updated_data.user_id
        and _curr_is_admin
        and not _target_is_admin
        and not _target_is_chief_admin
    ):  # ADMIN is only able to change USER* profiles
        target_user_id = profile_updated_data.user_id
    else:
        target_user_id = token_payload.user_id

    await update_profile_data(target_user_id, profile_updated_data)

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
        TEMPLATE__ACCESS_RENEW_REQUEST_EMAIL["subject"],
        TEMPLATE__ACCESS_RENEW_REQUEST_EMAIL["content"].format(
            url=__ACCESS_RENEW_URL_TEMPLATE.format(reset_token)
        )
    )

    return {
        "detail": "Please check email to renew access to TreS"
    }


async def profile__get_new_token(
    reset_token: str,
    __auth_obj: BurritoJWT = Depends(get_auth_core())
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

    tokens = await __auth_obj.create_token_pare(
        AuthTokenPayload(
            user_id=user.user_id,
            role=user.role.name
        )
    )
    return {
        "access_token": tokens["access_token"]
    }
