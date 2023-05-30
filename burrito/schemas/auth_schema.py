from pydantic import BaseModel


class AuthSettingsModel(BaseModel):
    """_summary_

    Authorization token model

    Args:
        authjwt_secret_key (str): token data
    """

    authjwt_secret_key: str = "secret"
#    authjwt_denylist_enabled = True


class UserPasswordLoginSchema(BaseModel):
    """_summary_

    User need to transfer this data to get access to API

    Args:
        login (str): user login
        password (str): user password
    """

    login: str
    password: str


class AuthResponseSchema(BaseModel):
    user_id: int
    login: str
    access_token: str
    refresh_token: str | None
