from pydantic import BaseModel


class UserPasswordLoginSchema(BaseModel):
    login: str
    password: str
