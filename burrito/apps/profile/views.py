from fastapi import Depends, status
from fastapi.responses import JSONResponse

from burrito.models.user_model import Users
from burrito.models.roles_model import Roles

from burrito.schemas.profile_schema import (
    ResponseProfileSchema,
    RequestUpdateProfileSchema
)

from burrito.utils.auth import AuthTokenPayload, BurritoJWT
from burrito.utils.converter import (
    FacultyConverter,
    GroupConverter
)
from burrito.utils.users_util import get_user_by_login, is_admin
from burrito.utils.hash_util import get_hash
from burrito.utils.validators import (
    is_valid_firstname,
    is_valid_lastname,
    is_valid_login,
    is_valid_email,
    is_valid_password,
    is_valid_phone
)

from .utils import (
    get_auth_core, get_user_by_id,
    check_permission,
    view_profile_by_user_id
)


async def profile__check_by_id(
    user_id: int,
) -> ResponseProfileSchema:
    """Return some data to check user profile"""

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
    if (
        profile_updated_data.user_id
        and profile_updated_data.user_id != token_payload.user_id
        and is_admin(token_payload.user_id)
    ):
        target_user_id = profile_updated_data.user_id
    else:
        target_user_id = token_payload.user_id

    current_user: Users | None = get_user_by_id(target_user_id)

    if is_valid_firstname(profile_updated_data.firstname):
        current_user.firstname = profile_updated_data.firstname

    if is_valid_lastname(profile_updated_data.lastname):
        current_user.lastname = profile_updated_data.lastname

    if is_valid_login(profile_updated_data.login):
        # user can provide their own login, so we should not raise en error
        if current_user.login != profile_updated_data.login and get_user_by_login(profile_updated_data.login):
            return JSONResponse(
                status_code=403,
                content={
                    "field": "login",
                    "detail": "User with the same login exists"
                }
            )

        current_user.login = profile_updated_data.login

    if is_valid_phone(profile_updated_data.phone):
        current_user.phone = profile_updated_data.phone

    if is_valid_email(profile_updated_data.email):
        current_user.email = profile_updated_data.email

    # check faculty
    if profile_updated_data.faculty:
        faculty_id = FacultyConverter.convert(profile_updated_data.faculty)
        if faculty_id:
            current_user.faculty = faculty_id

    # check group
    if profile_updated_data.group:
        group_id = GroupConverter.convert(profile_updated_data.group)
        if group_id:
            current_user.group = group_id

    if is_valid_password(profile_updated_data.password):
        current_user.password = get_hash(profile_updated_data.password)

    if profile_updated_data.role_id and Roles.get_or_none(Roles.role_id == profile_updated_data.role_id):
        current_user.role = profile_updated_data.role_id

    current_user.save()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Profile was updated"}
    )
