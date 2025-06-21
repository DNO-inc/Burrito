from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from burrito.models.m_email_code import EmailVerificationCode
from burrito.models.user_model import Users
from burrito.schemas.email_code import EmailVerificationCodeSchema
from burrito.schemas.registration_schema import RegistrationSchema
from burrito.utils.auth import AuthTokenPayload, create_token_pare
from burrito.utils.config_reader import get_config
from burrito.utils.converter import DivisionConverter, GroupConverter
from burrito.utils.email_util import tmp_send_email
from burrito.utils.hash_util import generate_email_code, get_hash
from burrito.utils.mongo_util import mongo_delete, mongo_insert, mongo_select
from burrito.utils.users_util import get_user_by_email_or_none

from .utils import create_user, get_user_by_login, is_valid_login, is_valid_password

EMAIL_VERIFICATIONS_TEMPLATE = """Добрий день,


Ваш запит на реєстрацію в проекті TreS було успішно оброблено.
Для завершення реєстрації, будь ласка, введіть нижче наведений код підтвердження:

{}

Будь ласка, уважно перевірте введений код та переконайтеся, що він відповідає наданому вам під час реєстрації.
Якщо у вас виникли будь-які труднощі чи потребуються додаткові вказівки, будь ласка, зв'яжіться з нашою службою підтримки.


З повагою,

Команда TreS
"""


async def registration__user_registration(
    user_data: RegistrationSchema
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

    if get_user_by_email_or_none(user_data.email):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "User with the same email exist"}
        )

    if mongo_select(
        EmailVerificationCode,
        login=user_data.login
    ):
        raise HTTPException(
            status_code=403,
            detail="User with the same login is in registration process"
        )

    for group_id in user_data.group_ids:
        GroupConverter.convert(group_id)
    DivisionConverter.convert(user_data.division_id)

    verification_code = generate_email_code()
    mongo_insert(
        EmailVerificationCode(
            hashed_code=get_hash(
                verification_code,
                get_config().BURRITO_JWT_SECRET.encode()
            ),
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            login=user_data.login,
            password=get_hash(user_data.password),
            group_ids=user_data.group_ids,
            division_id=user_data.division_id,
            phone=user_data.phone,
            email=user_data.email
        )
    )

    tmp_send_email(
        user_data.email,
        "Підтвердження реєстрації в TreS",
        EMAIL_VERIFICATIONS_TEMPLATE.format(verification_code)
    )

    return {
        "status": "OK"
    }


async def registration__verify_email(
    verification_data: EmailVerificationCodeSchema
):
    email_code = mongo_select(
        EmailVerificationCode,
        hashed_code=get_hash(
            verification_data.email_code,
            get_config().BURRITO_JWT_SECRET.encode()
        ),
        email=verification_data.email
    )

    if not email_code:
        raise HTTPException(
            status_code=403,
            detail="Invalid code or email received"
        )
    email_code = email_code[0]

    current_user: Users | None = create_user(
        RegistrationSchema(
            **email_code
        )
    )

    if current_user:
        result = {
            **create_token_pare(
                AuthTokenPayload(
                    user_id=current_user.user_id,
                    role=current_user.role.name
                )
            ),
            "user_id": current_user.user_id
        }

        mongo_delete(
            EmailVerificationCode,
            _id=email_code["_id"]
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "..."}
    )
