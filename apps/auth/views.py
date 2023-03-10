
from fastapi import HTTPException, Depends
from fastapi_jwt_auth import AuthJWT

from schemas.user_schema import UserPasswordLoginSchema
from schemas.auth_schema import AuthSettingsModel



@AuthJWT.load_config
def get_config():
    return AuthSettingsModel()


def password_login(user: UserPasswordLoginSchema, Authorize: AuthJWT=Depends()):
    if user.login != "test" or user.password != "test":
        raise HTTPException(status_code=401,detail="Bad username or password")

    access_token = Authorize.create_access_token(subject=user.login)
    return {"access_token": access_token}


def token_login(Authorize: AuthJWT=Depends()):
    ...

