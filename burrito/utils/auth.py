from fastapi_jwt_auth import AuthJWT

from burrito.schemas.auth_schema import AuthSettingsModel


@AuthJWT.load_config
def get_auth_config():
    return AuthSettingsModel()


def get_auth_core():
    return AuthJWT
