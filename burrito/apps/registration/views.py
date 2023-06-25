from fastapi import Depends, status
from fastapi.responses import JSONResponse

from fastapi_jwt_auth import AuthJWT

from burrito.schemas.registration_schema import RegistrationSchema

from burrito.models.user_model import Users

from burrito.utils.converter import GroupConverter, FacultyConverter

from burrito.utils.auth import get_auth_core
from burrito.utils.auth_token_util import (
    AuthTokenPayload,
    create_access_token_payload
)

from .utils import (
    get_hash,
    create_user_tmp_foo, get_user_by_login,
    is_valid_login, is_valid_password
)


async def registration__user_registration(
    user_data: RegistrationSchema,
    Authorize: AuthJWT = Depends(get_auth_core())
):
    """Handle user registration"""

    if not is_valid_login(user_data.login):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "Invalid login"}
        )

    if not is_valid_password(user_data.password):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "Invalid password"}
        )

    if get_user_by_login(user_data.login):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "User with the same login exist"}
        )

    current_user: Users | None = create_user_tmp_foo(
        user_data.login,
        get_hash(user_data.password),
        GroupConverter.convert(user_data.group),
        FacultyConverter.convert(user_data.faculty)
    )

    if current_user:
        access_token = Authorize.create_access_token(
            subject=create_access_token_payload(
                AuthTokenPayload(
                    user_id=current_user.user_id,
                    role=current_user.role.name
                )
            )
        )
        refresh_token = Authorize.create_refresh_token(
            subject=current_user.user_id
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "user_id": current_user.user_id,
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "..."}
    )
