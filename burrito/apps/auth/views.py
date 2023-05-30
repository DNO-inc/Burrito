from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from burrito.schemas.auth_schema import (
    AuthResponseSchema,
    UserPasswordLoginSchema
)

from burrito.models.user_model import Users

from burrito.utils.auth_token_util import (
    create_access_token_payload,
    read_access_token_payload,
    AuthTokenPayload
)

from burrito.utils.users_util import (
    get_user_by_id
)

from .utils import (
    get_auth_core,
    get_user_by_login,
    compare_password
)


def auth__password_login(
        user_login_data: UserPasswordLoginSchema,
        Authorize: AuthJWT = Depends(get_auth_core())
        ):
    """Authentication by login and password"""

    user: Users | None = get_user_by_login(user_login_data.login)

    if user:
        # if user login exist we can compare password and hashed password

        if compare_password(user_login_data.password, user.password):
            access_token = Authorize.create_access_token(
                subject=create_access_token_payload(
                    AuthTokenPayload(
                        user_id=user.user_id,
                        role=user.role.name
                    )
                )
            )
            refresh_token = Authorize.create_refresh_token(
                subject=user.user_id
            )

            return AuthResponseSchema(
                user_id=user.user_id,
                login=user.login,
                access_token=access_token,
                refresh_token=refresh_token
            )

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Password is incorrect"}
        )

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Login is not exist"}
    )


def auth__token_login(Authorize: AuthJWT = Depends()):
    """
        Authentication by access token. It will return new access token ^_^
    """

    Authorize.jwt_required()

    token_payload: AuthTokenPayload = read_access_token_payload(
        Authorize.get_jwt_subject()
    )

    user: Users | None = get_user_by_id(token_payload.user_id)

    return AuthResponseSchema(
        user_id=user.user_id,
        login=user.login,
        access_token=Authorize.create_access_token(
            subject=create_access_token_payload(
                token_data=token_payload
            )
        )
    )
