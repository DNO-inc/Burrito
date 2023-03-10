
from fastapi import Depends

from fastapi_jwt_auth import AuthJWT



async def my_account_check(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()

    return {"my_data": [1, 2, "hello", current_user]}


