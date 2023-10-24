from pydantic import BaseModel


class EmailVerificationCodeSchema(BaseModel):
    email: str
    email_code: str
