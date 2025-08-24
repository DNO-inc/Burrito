from typing import Optional

from pydantic import BaseModel


class RegistrationSchema(BaseModel):
    firstname: str
    lastname: str

    login: str
    password: str
    group: Optional[int] = None
    faculty: int

    phone: Optional[str] = None
    email: str
