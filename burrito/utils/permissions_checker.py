from fastapi import HTTPException
from pydantic import BaseModel

from burrito.models.role_permissions_model import RolePermissions
from burrito.models.user_model import Users
from burrito.utils.users_util import get_user_by_id


class EndpointPermissionError(HTTPException):
    ...


class PermissionMetaData(BaseModel):
    user_id: int
    role_name: str


def check_permission(user: Users | int, permission_list: set[str] | None = None):
    if isinstance(user, int):
        user = get_user_by_id(user)

    if permission_list is None:
        permission_list = set()

    current_user_permissions: set[str] = set()
    for item in RolePermissions.select().where(
        RolePermissions.role == user.role
    ):
        current_user_permissions.add(item.permission.name)

    # if permission_list is empty we can skip permission verification
    # else we should check current user permissions
    is_accepted = not bool(permission_list)
    for permission in permission_list:
        if permission in current_user_permissions:
            is_accepted = True
            break

    if not is_accepted:
        raise EndpointPermissionError(
            status_code=403,
            detail="You have not permissions to interact with this resource"
        )

    return PermissionMetaData(
        user_id=user.user_id,
        role_name=user.role.name
    )
