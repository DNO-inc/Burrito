from fastapi import Depends, status
from fastapi.responses import JSONResponse

from burrito.schemas.auth_schema import (
    AuthResponseSchema,
    UserPasswordLoginSchema
)

from burrito.models.user_model import Users

from burrito.utils.logger import get_logger
from burrito.utils.auth import (
    AuthTokenPayload,
    BurritoJWT
)

from burrito.utils.users_util import (
    get_user_by_id
)

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


async def auth__token_login(__auth_obj: BurritoJWT = Depends(get_auth_core())):
    """
        Authentication by access token. It will return new access token ^_^
    """

    token_payload: AuthTokenPayload = await __auth_obj.verify_token()

    user: Users | None = get_user_by_id(token_payload.user_id)

    new_access_token = await __auth_obj.push_token(
        token_payload,
        "access"
    )

    get_logger().info(
        f"""
            Token login:
                * user_id: {user.user_id}
                * login: {user.login}
                * tokens: {new_access_token}

        """
    )

    return AuthResponseSchema(
        user_id=user.user_id,
        login=user.login,
        access_token=new_access_token
    )
