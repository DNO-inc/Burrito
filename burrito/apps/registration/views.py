from fastapi import Depends, status
from fastapi.responses import JSONResponse

from burrito.schemas.registration_schema import RegistrationSchema

from burrito.models.user_model import Users

from burrito.utils.auth import get_auth_core, BurritoJWT, AuthTokenPayload

from .utils import (
    create_user, get_user_by_login,
    is_valid_login, is_valid_password
)


async def registration__user_registration(
    user_data: RegistrationSchema,
    __auth_obj: BurritoJWT = Depends(get_auth_core())
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

    current_user: Users | None = create_user(user_data)

    if current_user:
        result = (await __auth_obj.create_token_pare(
            AuthTokenPayload(
                user_id=current_user.user_id,
                role=current_user.role.name
            )
        )) | {"user_id": current_user.user_id}

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "..."}
    )
