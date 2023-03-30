from pydantic import BaseModel


class UserPasswordLoginSchema(BaseModel):
    """_summary_

    User need to transfer this data to get access to API

    Args:
        login (str): user login
        password (str): user password
    """

    login: str
    password: str
