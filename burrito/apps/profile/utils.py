from secrets import token_urlsafe
from fastapi import HTTPException
from playhouse.shortcuts import model_to_dict

from burrito.utils.auth import get_auth_core
from burrito.utils.users_util import (
    get_user_by_id,
    get_user_by_login
)

from burrito.utils.permissions_checker import check_permission

from burrito.models.user_model import Users
from burrito.models.faculty_model import Faculties
from burrito.models.group_model import Groups
from burrito.models.role_permissions_model import RolePermissions

from burrito.schemas.profile_schema import (
    ResponseProfileSchema,
    ResponseRoleSchema,
    RequestUpdateProfileSchema
)
from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.group_schema import GroupResponseSchema

from burrito.utils.converter import (
    FacultyConverter,
    GroupConverter
)
from burrito.utils.hash_util import get_hash
from burrito.utils.validators import (
    is_valid_firstname,
    is_valid_lastname,
    is_valid_login,
    is_valid_password,
    is_valid_phone
)

__all__ = (
    "get_auth_core",
    "get_user_by_id",
    "check_permission",
    "view_profile_by_user_id"
)


async def view_profile_by_user_id(user_id: int) -> ResponseProfileSchema | None:
    current_user: Users | None = get_user_by_id(user_id)

    faculty_object: Faculties | None = current_user.faculty
    group_object: Groups | None = current_user.group

    return ResponseProfileSchema(
        firstname=current_user.firstname,
        lastname=current_user.lastname,
        login=current_user.login,
        faculty=FacultyResponseSchema(**model_to_dict(faculty_object)) if faculty_object else None,
        group=GroupResponseSchema(**model_to_dict(group_object)) if group_object else None,
        phone=current_user.phone,
        email=current_user.email,
        role=ResponseRoleSchema(
            role_id=current_user.role.role_id,
            name=current_user.role.name,
            permission_list=list(
                i.permission.name for i in RolePermissions.select(
                    RolePermissions.permission
                ).where(
                    RolePermissions.role == current_user.role.role_id
                )
            )
        ),
        registration_date=str(current_user.registration_date)
    )


async def update_profile_data(
    user_id: int,
    profile_updated_data: RequestUpdateProfileSchema | None = RequestUpdateProfileSchema()
) -> None:
    current_user: Users | None = get_user_by_id(user_id)

    if is_valid_firstname(profile_updated_data.firstname):
        current_user.firstname = profile_updated_data.firstname

    if is_valid_lastname(profile_updated_data.lastname):
        current_user.lastname = profile_updated_data.lastname

    if is_valid_login(profile_updated_data.login):
        # user can provide their own login, so we should not raise en error
        if current_user.login != profile_updated_data.login and get_user_by_login(profile_updated_data.login):
            raise HTTPException(
                status_code=403,
                detail="User with the same login exists"
            )

        current_user.login = profile_updated_data.login

    if is_valid_phone(profile_updated_data.phone):
        current_user.phone = profile_updated_data.phone

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

    current_user.save()


def generate_reset_token() -> str:
    return token_urlsafe(64)
