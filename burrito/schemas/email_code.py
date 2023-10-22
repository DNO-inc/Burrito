from pydantic import BaseModel


class EmailVerificationCodeSchema(BaseModel):
    email_code: str
