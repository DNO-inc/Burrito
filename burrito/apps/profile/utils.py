from burrito.utils.auth import get_auth_core
from burrito.utils.db_utils import get_user_by_id

from burrito.utils.base_view import BaseView, status
from burrito.utils.permissions_checker import check_permission

from burrito.models.user_model import Users
from burrito.models.faculty_model import Faculties
from burrito.models.group_model import Groups

from burrito.schemas.profile_schema import ResponseProfileSchema

__all__ = (
    "get_auth_core",
    "get_user_by_id",
    "BaseView",
    "status",
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
        faculty=faculty_object.name if faculty_object else None,
        group=group_object.name if group_object else None,
        phone=current_user.phone,
        email=current_user.email,
        registration_date=str(current_user.registration_date)
    )
