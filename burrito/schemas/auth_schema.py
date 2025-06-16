from pydantic import BaseModel


class AuthSettingsModel(BaseModel):
    """
    Authorization token model

    Args:
        authjwt_secret_key (str): token data
    """

    authjwt_secret_key: str = "secret"
#    authjwt_denylist_enabled = True


class UserPasswordLoginSchema(BaseModel):
    """
    User need to transfer this data to get access to API

    Args:
        login (str): user login
        password (str): user password
    """

    login: str
    password: str


class UserKeyLoginSchema(BaseModel):
    """
    User need to transfer this data to get access to API

    Args:
        key (str): user key from SSU Cabinet
        token (str): app token from SSU Cabinet
    """

    key: str
    token: str


class AuthResponseSchema(BaseModel):
    user_id: int
    login: str
    access_token: str
    refresh_token: str | None


class KeyAuthResponseSchema(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str | None
