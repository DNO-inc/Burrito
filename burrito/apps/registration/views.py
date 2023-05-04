from fastapi.responses import JSONResponse

from burrito.schemas.user_schema import (
    UserPasswordLoginSchema,
    UserVerificationCode
)

from .utils import (
    get_hash,
    create_user, get_user_by_login,
    is_valid_login, is_valid_password,
    status
)


async def registration_main(user_data: UserPasswordLoginSchema):
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

    user_id_value: int | None = create_user(
        user_data.login,
        get_hash(user_data.password)
    )

    if user_id_value:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"user_id": user_id_value}
        )

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "'\\_(-_-)_/'"}
    )


async def check_verification_code(code_object: UserVerificationCode):
    ...
