import httpx
from fastapi import Depends, status
from fastapi.responses import JSONResponse

from burrito.models.user_model import Users
from burrito.plugins.loader import PluginLoader
from burrito.schemas.auth_schema import (
    AuthResponseSchema,
    KeyAuthResponseSchema,
    UserKeyLoginSchema,
    UserPasswordLoginSchema,
)
from burrito.utils.auth import (
    AuthTokenPayload,
    create_access_token,
    create_token_pare,
    delete_refresh_token,
    get_current_user,
    rotate_refresh_token,
)
from burrito.utils.logger import get_logger
from burrito.utils.users_util import create_user_with_cabinet, get_user_by_cabinet_id

from .utils import (
    compare_password,
    get_cabinet_key,
    get_user_by_login,
    put_cabinet_key,
    remove_cabinet_key,
)


async def auth__password_login(
    user_login_data: UserPasswordLoginSchema,
):
    """Authentication by login and password"""

    user: Users | None = get_user_by_login(user_login_data.login)

    if user:
        # if user login exist we can compare password and hashed password

        if compare_password(user_login_data.password, user.password):
            tokens = create_token_pare(
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
    user_login_data: UserKeyLoginSchema
):
    """Authentication by key from SSU Cabinet"""

    try:
        cabinet_profile = PluginLoader.execute_plugin(
            "third_party_auth",
            key=user_login_data.key,
            token=user_login_data.token
        )
    except (KeyError, ValueError) as exc:
        get_logger().error(exc)

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Failed to get user data from SSU Cabinet"}
        )

    user: Users | None = get_user_by_cabinet_id(cabinet_profile["user_id"])

    if user:
        # if user login exist we just return auth schema

        tokens = create_token_pare(
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

            """
        )

        put_cabinet_key(user, user_login_data.key)

        return KeyAuthResponseSchema(
            user_id=user.user_id,
            **tokens
        )

    # So, this is the first login. Let's create a locale user record

    new_user: Users | None = create_user_with_cabinet(
        cabinet_id=cabinet_profile["user_id"],
        firstname=cabinet_profile["firstname"],
        lastname=cabinet_profile["lastname"],
        division=cabinet_profile["division"],
        group=cabinet_profile["group"],
        email=cabinet_profile["email"],
    )

    if not new_user:
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={"detail": "Failed to create a new user"}
        )

    get_logger().info(
        f"""
            Key login:
                * user_id: {new_user.user_id}
                * name: {new_user.firstname} {new_user.lastname}

        """
    )

    put_cabinet_key(new_user, user_login_data.key)

    return KeyAuthResponseSchema(
        user_id=new_user.user_id,
        **create_token_pare(
            AuthTokenPayload(
                user_id=new_user.user_id,
                role=new_user.role.name
            )
        )
    )


async def auth__token_refresh(
    _auth_obj: tuple[Users, str] = Depends(rotate_refresh_token)
):
    user = _auth_obj[0]

    payload = AuthTokenPayload(
        user_id=user.user_id,
        role=user.role.name
    )

    return AuthResponseSchema(
        user_id=user.user_id,
        login=user.login,
        access_token=create_access_token(payload),
        refresh_token=_auth_obj[1]
    )


async def auth_delete_refresh_token(
    _curr_user: Users = Depends(delete_refresh_token)
):
    return JSONResponse(
        content={"detail": "Refresh tokens was deleted"},
        status_code=200
    )


async def auth__logout(
    _curr_user: Users = Depends(get_current_user())
):
    cabinet_key = get_cabinet_key(_curr_user)
    if not cabinet_key:
        return JSONResponse(
            content={"detail": "Service key is expired"},
            status_code=403
        )

    try:
        async with httpx.AsyncClient() as client:
            await client.get(
                f"https://cabinet.sumdu.edu.ua/api/logout?key={cabinet_key}"
            )

        remove_cabinet_key(_curr_user)

    except Exception as exc:
        get_logger().error(exc)
        return JSONResponse(
            content={"detail": "Something gone wrong"},
            status_code=200
        )

    return JSONResponse(
        content={"detail": "You have successfully logged out"},
        status_code=200
    )
