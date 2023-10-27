from fastapi import Depends, status
from fastapi.responses import JSONResponse

from burrito.schemas.profile_schema import (
    ResponseProfileSchema,
    RequestUpdateProfileSchema
)

from burrito.utils.auth import AuthTokenPayload, BurritoJWT
from burrito.utils.users_util import is_admin, is_chief_admin

from .utils import (
    get_auth_core,
    check_permission,
    view_profile_by_user_id,
    update_profile_data
)


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
