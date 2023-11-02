from burrito.models.m_basic_model import MongoBaseModel, MongoTTLModel


class EmailVerificationCode(MongoBaseModel, MongoTTLModel):
    hashed_code: str

    firstname: str
    lastname: str

    login: str
    password: str
    group: int | None = None
    faculty: int

    phone: str | None = None
    email: str

    class Meta:
        table_name: str = "email_verification_codes"
