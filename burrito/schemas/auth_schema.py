from pydantic import BaseModel


class AuthSettingsModel(BaseModel):
    """_summary_

    Authorization token model

    Args:
        authjwt_secret_key (str): token data
    """

    authjwt_secret_key: str = "secret"
