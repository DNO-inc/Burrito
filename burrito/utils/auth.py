from fastapi_jwt_auth import AuthJWT

from burrito.schemas.auth_schema import AuthSettingsModel


@AuthJWT.load_config
def get_auth_config():
    return AuthSettingsModel()


# TODO: make storage for revoked tokens
denylist = set()


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in denylist


def get_auth_core():
    return AuthJWT
