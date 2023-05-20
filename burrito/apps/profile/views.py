from fastapi import Depends, status
from fastapi.responses import JSONResponse

from fastapi_jwt_auth import AuthJWT

from burrito.models.user_model import Users

from burrito.schemas.profile_schema import (
    ResponseProfileSchema,
    RequestUpdateProfileSchema
)

from burrito.utils.converter import (
    FacultyStrToInt,
    GroupStrToInt
)

from .utils import (
    get_auth_core, get_user_by_id,
    check_permission,
    view_profile_by_user_id
)


@check_permission
async def profile__check_my_profile(
    Authorize: AuthJWT = Depends(get_auth_core())
) -> ResponseProfileSchema:
    """Return some data to check user profile"""

    Authorize.jwt_required()

    return await view_profile_by_user_id(Authorize.get_jwt_subject())


@check_permission
async def profile__check_by_id(
    user_id: int,
) -> ResponseProfileSchema:
    """Return some data to check user profile"""

    return await view_profile_by_user_id(user_id)


@check_permission
async def profile__update_my_profile(
    profile_updated_data: RequestUpdateProfileSchema,
    Authorize: AuthJWT = Depends(get_auth_core())
):
    """Update profile data"""

    Authorize.jwt_required()

    user_id = Authorize.get_jwt_subject()
    current_user: Users | None = get_user_by_id(user_id)

    if profile_updated_data.firstname:
        current_user.firstname = profile_updated_data.firstname

    if profile_updated_data.lastname:
        current_user.lastname = profile_updated_data.lastname

    if profile_updated_data.phone:
        current_user.phone = profile_updated_data.phone

    if profile_updated_data.email:
        current_user.email = profile_updated_data.email

    # check faculty
    faculty_id = FacultyStrToInt.convert(profile_updated_data.faculty)
    if faculty_id and profile_updated_data.faculty:
        current_user.faculty = faculty_id

    # check group
    group_id = GroupStrToInt.convert(profile_updated_data.group)
    if group_id and profile_updated_data.group:
        current_user.group = group_id

    current_user.save()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Profile was updated"}
    )
