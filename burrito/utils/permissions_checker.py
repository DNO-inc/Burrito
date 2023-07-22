from fastapi import HTTPException

from burrito.models.user_model import Users
from burrito.models.role_permissions_model import RolePermissions

from burrito.utils.users_util import get_user_by_id


class EndpointPermissionError(HTTPException):
    ...


def check_permission(token_payload, permission_list: set[str] = set()):
    current_user: Users | None = get_user_by_id(
        token_payload.user_id
    )

    current_user_permissions: set[str] = set()
    for item in RolePermissions.select().where(
        RolePermissions.role == current_user.role
    ):
        current_user_permissions.add(item.permission.name)

    if not permission_list.issubset(current_user_permissions):
        raise EndpointPermissionError(
            status_code=403,
            detail="You have not permissions to interact with this resource"
        )
