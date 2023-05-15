from fastapi.responses import JSONResponse

from burrito.schemas.user_schema import (
    UserVerificationCode
)
from burrito.schemas.registration_schema import RegistrationSchema

from .utils import (
    get_hash,
    create_user_tmp_foo, get_user_by_login,
    is_valid_login, is_valid_password,
    BaseView,
    status,
    check_permission
)


class RegistrationMainView(BaseView):
    _permissions: list[str] = [""]

    @staticmethod
    @check_permission
    async def post(user_data: RegistrationSchema):
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

        user_id_value: int | None = create_user_tmp_foo(
            user_data.login,
            get_hash(user_data.password),
            user_data.group,
            user_data.faculty
        )

        if user_id_value:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"user_id": user_id_value}
            )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "Group or faculty is not valid"}
        )


async def check_verification_code(code_object: UserVerificationCode):
    ...
