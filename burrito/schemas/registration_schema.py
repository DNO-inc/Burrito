from pydantic import BaseModel


class RegistrationSchema(BaseModel):
    firstname: str
    lastname: str

    login: str
    password: str
    group_ids: list[int] = []
    division_id: int

    phone: str | None
    email: str
