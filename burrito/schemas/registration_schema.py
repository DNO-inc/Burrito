from pydantic import BaseModel


class RegistrationSchema(BaseModel):
    firstname: str
    lastname: str

    login: str
    password: str
    group: int
    faculty: int

    phone: str | None
    email: str | None
