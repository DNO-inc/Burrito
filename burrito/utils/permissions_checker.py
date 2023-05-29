from functools import wraps

from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT

from burrito.models.user_model import Users
from burrito.models.role_permissions_model import RolePermissions

from burrito.utils.db_utils import get_user_by_id

from burrito.utils.auth_token_util import (
    read_access_token_payload,
    AuthTokenPayload
)


class EndpointPermissionError(HTTPException):
    ...


def check_permission(permission_list: set[str] = set()):

    def function_wrap(func):

        @wraps(func)
        async def wrap(*args, **kwargs):
            auth_core: AuthJWT | None = None

            if not auth_core:
                for i, arg_value in kwargs.items():
                    if isinstance(arg_value, AuthJWT):
                        auth_core = arg_value
                        break

            if not auth_core:
                for arg_value in args:
                    if isinstance(arg_value, AuthJWT):
                        auth_core = arg_value
                        break

            if auth_core:
                auth_core.jwt_required()

                token_payload: AuthTokenPayload = read_access_token_payload(
                    auth_core.get_jwt_subject()
                )
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

            return await func(*args, **kwargs)

        return wrap

    return function_wrap
