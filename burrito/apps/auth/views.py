from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from burrito.schemas.user_schema import UserPasswordLoginSchema

from burrito.models.user_model import Users

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
                subject=user.user_id
            )
            refresh_token = Authorize.create_refresh_token(
                subject=user.user_id
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "user_id": user.user_id,
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
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

    return {
        "access_token": Authorize.create_access_token(
            subject=Authorize.get_jwt_subject()
        )
    }
