from playhouse.shortcuts import model_to_dict

from burrito.utils.auth import get_auth_core
from burrito.utils.users_util import get_user_by_id

from burrito.utils.permissions_checker import check_permission

from burrito.models.user_model import Users
from burrito.models.faculty_model import Faculties
from burrito.models.group_model import Groups

from burrito.schemas.profile_schema import ResponseProfileSchema
from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.group_schema import GroupResponseSchema


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
        registration_date=str(current_user.registration_date)
    )
