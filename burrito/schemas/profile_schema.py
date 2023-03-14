from pydantic import BaseModel


class UpdateProfileSchema(BaseModel):
    firstname: str | None
    lastname: str | None
    phone: str | None
    email: str | None
