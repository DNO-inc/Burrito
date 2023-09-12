from fastapi import Depends, status
from fastapi.responses import JSONResponse

from burrito.models.user_model import Users

from burrito.schemas.profile_schema import (
    ResponseProfileSchema,
    RequestUpdateProfileSchema
)

from burrito.utils.auth import AuthTokenPayload, BurritoJWT
from burrito.utils.converter import (
    FacultyConverter,
    GroupConverter
)
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

    current_user: Users | None = get_user_by_id(token_payload.user_id)

    if is_valid_firstname(profile_updated_data.firstname):
        current_user.firstname = profile_updated_data.firstname

    if is_valid_lastname(profile_updated_data.lastname):
        current_user.lastname = profile_updated_data.lastname

    if is_valid_login(profile_updated_data.login):
        current_user.login = profile_updated_data.login

    if is_valid_phone(profile_updated_data.phone):
        current_user.phone = profile_updated_data.phone

    if is_valid_email(profile_updated_data.email):
        current_user.email = profile_updated_data.email

    # check faculty
    faculty_id = FacultyConverter.convert(profile_updated_data.faculty)
    if faculty_id and profile_updated_data.faculty:
        current_user.faculty = faculty_id

    # check group
    group_id = GroupConverter.convert(profile_updated_data.group)
    if group_id and profile_updated_data.group:
        current_user.group = group_id

    if is_valid_password(profile_updated_data.password):
        current_user.password = get_hash(profile_updated_data.password)

    current_user.save()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Profile was updated"}
    )
