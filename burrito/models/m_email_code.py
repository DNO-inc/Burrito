from burrito.models.m_basic_model import MongoBaseModel


class EmailVerificationCode(MongoBaseModel):
    hashed_code: str

    firstname: str
    lastname: str

    login: str
    password: str
    group: int | None = None
    faculty: int

    phone: str | None
    email: str | None

    class Meta:
        table_name: str = "email_verification_codes"
