import json

import aioredis

from burrito.utils.singleton_pattern import singleton

from burrito.schemas.user_schema import UserPasswordLoginSchema
from burrito.utils.hash_util import get_hash, get_verification_code


def _dict_to_json(data: dict) -> str:
    return json.dumps(data)


def _json_to_dict(data: str) -> dict:
    return json.loads(data)


REDIS_REGISTRATION_DATA_TTL: int = 300


@singleton
class BurritoRedis(aioredis.Redis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def is_user_exist(self, user_login: str) -> bool:
        """_summary_

        Args:
            user (str): user login

        Returns:
            bool: is user already exists in redis storage
        """

        return bool(await self.get("tmp_user_login__" + user_login))

    async def put_user_login_data(self, user: UserPasswordLoginSchema) -> str:
        """_summary_

        Put user data into redis storage

        Args:
            user (UserPasswordLoginSchema): users data
        """

        tmp_verification_code = get_verification_code()
        await self.set(
            "tmp_user_login__" + user.login,
            _dict_to_json(
                {
                    "password": get_hash(user.password),
                    "verification_code": tmp_verification_code
                }
            ),
            ex=REDIS_REGISTRATION_DATA_TTL
        )
        return tmp_verification_code

    async def get_user_by_login(self, user_login: str) -> dict:
        """_summary_

        Get user data located in redis storage

        Args:
            user_login (str): login
        """

        return {"login": user_login} + _json_to_dict(
            await self.get("tmp_user_login__" + user_login)
        )


def get_redis_cursor() -> BurritoRedis:
    """_summary_

    Returns:
        BurritoRedis: redis cursor object
    """

    return
#    return BurritoRedis(
#        host="localhost",
#        port=6379,
#        password="root"
#    )
