from fastapi import Depends, status
from fastapi.responses import JSONResponse

from burrito.schemas.auth_schema import (
    AuthResponseSchema,
    UserPasswordLoginSchema,
    UserKeyLoginSchema,
    KeyAuthResponseSchema
)

from burrito.models.user_model import Users

from burrito.utils.logger import get_logger
from burrito.utils.permissions_checker import check_permission
from burrito.utils.auth import (
    AuthTokenPayload,
    BurritoJWT,
    create_access_token
)
from burrito.utils.users_util import (
    get_user_by_id_or_none, get_user_by_id, create_user_with_cabinet
)

from burrito.plugins.loader import PluginLoader


from .utils import (
    get_auth_core,
    get_user_by_login,
    compare_password
)


async def auth__password_login(
        user_login_data: UserPasswordLoginSchema,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Authentication by login and password"""

    user: Users | None = get_user_by_login(user_login_data.login)

    if user:
        # if user login exist we can compare password and hashed password

        if compare_password(user_login_data.password, user.password):
            tokens = await __auth_obj.create_token_pare(
                AuthTokenPayload(
                    user_id=user.user_id,
                    role=user.role.name
                )
            )

            get_logger().info(
                f"""
                    Password login:
                        * user_id: {user.user_id}
                        * login: {user_login_data.login}
                        * tokens: {tokens}

                """
            )

            return AuthResponseSchema(
                user_id=user.user_id,
                login=user.login,
                **tokens
            )

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Password is incorrect"}
        )

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Login is not exist"}
    )


async def auth__key_login(
        user_login_data: UserKeyLoginSchema,
        __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    """Authentication by key from SSU Cabinet"""

    try:
        cabinet_profile = PluginLoader.execute_plugin(
            "third_party_auth",
            key=user_login_data.key,
            token=user_login_data.token
        )
    except (KeyError, ValueError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Failed to get user data from SSU Cabinet"}
        )

    user: Users | None = get_user_by_id_or_none(cabinet_profile["user_id"])

    if user:
        # if user login exist we just return auth schema

        tokens = await __auth_obj.create_token_pare(
            AuthTokenPayload(
                user_id=user.user_id,
                role=user.role.name
            )
        )

        get_logger().info(
            f"""
                Key login:
                    * user_id: {user.user_id}
                    * name: {user.firstname} {user.lastname}
                    * tokens: {tokens}

            """
        )

        return KeyAuthResponseSchema(
            user_id=user.user_id,
            **tokens
        )

    if not user:

        # So, this is the first login. Let's create a locale user record

        new_user: Users | None = create_user_with_cabinet(
            user_id=cabinet_profile["user_id"],
            firstname=cabinet_profile["firstname"],
            lastname=cabinet_profile["lastname"],
            faculty=cabinet_profile["faculty"],
            group=cabinet_profile["group"],
            email=cabinet_profile["email"],
        )

        if new_user:
            result = {"user_id": new_user.user_id} | (await __auth_obj.create_token_pare(
                AuthTokenPayload(
                    user_id=new_user.user_id,
                    role=new_user.role.name
                )
            ))

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=result
            )

        if not new_user:
            return JSONResponse(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                content={"detail": "Failed to create a new user"}
            )

        tokens = await __auth_obj.create_token_pare(
            AuthTokenPayload(
                user_id=user.user_id,
                role=user.role.name
            )
        )

        get_logger().info(
            f"""
                Key login:
                    * user_id: {user.user_id}
                    * name: {user.firstname} {user.lastname}
                    * tokens: {tokens}

            """
        )

        return KeyAuthResponseSchema(
            user_id=user.user_id,
            **tokens
        )


async def auth__token_refresh(__auth_obj: BurritoJWT = Depends(get_auth_core())):
    token_payload: AuthTokenPayload = await __auth_obj.require_refresh_token()
    check_permission(token_payload)

    user: Users | None = get_user_by_id(token_payload.user_id)

    return AuthResponseSchema(
        user_id=user.user_id,
        login=user.login,
        access_token=create_access_token(token_payload),
        refresh_token=(await __auth_obj.rotate_refresh_token())
    )


async def auth_delete_refresh_token(__auth_obj: BurritoJWT = Depends(get_auth_core())):
    token_payload: AuthTokenPayload = await __auth_obj.require_refresh_token()
    check_permission(token_payload)

    get_user_by_id(token_payload.user_id)

    await __auth_obj.delete_refresh_token()

    return JSONResponse(
        content={"detail": "Refresh tokens was deleted"},
        status_code=200
    )
