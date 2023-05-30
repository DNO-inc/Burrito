from pydantic import BaseModel


class AuthSettingsModel(BaseModel):
    """_summary_

    Authorization token model

    Args:
        authjwt_secret_key (str): token data
    """

    authjwt_secret_key: str = "secret"
#    authjwt_denylist_enabled = True


class AuthResponseSchema(BaseModel):
    user_id: int
    login: str
    access_token: str
    refresh_token: str | None
