from pydantic import BaseModel


class RegistrationSchema(BaseModel):
    login: str
    password: str
    group: str
    faculty: str
