
from pydantic import BaseModel



class UserPasswordLoginSchema(BaseModel):
    def __init__(__pydantic_self__, **data: Any):
        super().__init__(data)
        __pydantic_self__.username = None

    login: str
    password: str


