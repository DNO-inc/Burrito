from burrito.models.m_basic_model import MongoBaseModel, MongoTTLModel


class EmailVerificationCode(MongoBaseModel, MongoTTLModel):
    hashed_code: str

    firstname: str
    lastname: str

    login: str
    password: str
    group_id: int | None = None
    division_id: int

    phone: str | None = None
    email: str

    class Meta:
        table_name: str = "email_verification_codes"
