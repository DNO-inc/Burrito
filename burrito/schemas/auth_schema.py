from pydantic import BaseModel


class AuthSettingsModel(BaseModel):
    authjwt_secret_key: str = "secret"
