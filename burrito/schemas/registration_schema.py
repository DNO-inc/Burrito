from pydantic import BaseModel


class RegistrationSchema(BaseModel):
    firstname: str
    lastname: str

    login: str
    password: str
    group_id: int | None = None
    division_id: int

    phone: str | None
    email: str
