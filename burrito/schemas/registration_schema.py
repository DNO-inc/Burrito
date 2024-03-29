from pydantic import BaseModel


class RegistrationSchema(BaseModel):
    firstname: str
    lastname: str

    login: str
    password: str
    group: int | None = None
    faculty: int

    phone: str | None
    email: str
