from burrito.models.user_model import Users
from burrito.utils.config_reader import get_config
from burrito.utils.hash_util import compare_password
from burrito.utils.logger import get_logger
from burrito.utils.redis_utils import get_redis_connector
from burrito.utils.users_util import get_user_by_id, get_user_by_login

__all__ = (
    "get_user_by_login",
    "get_user_by_id",
    "compare_password",
)


redis_cabinet_key = "cabinet_key__{}"
CABINET_KEY_TTL: int = get_config().BURRITO_JWT_REFRESH_TTL


def put_cabinet_key(user: Users, cabinet_key: str):
    get_redis_connector().set(
        redis_cabinet_key.format(user.user_id),
        cabinet_key,
        ex=CABINET_KEY_TTL
    )
    get_logger().info(f"Adding new key for {user.user_id}")


def get_cabinet_key(user: Users):
    cabinet_key: bytes = get_redis_connector().get(
        redis_cabinet_key.format(user.user_id)
    )

    if cabinet_key and isinstance(cabinet_key, bytes):
        return cabinet_key.decode()

    return cabinet_key


def remove_cabinet_key(user: Users):
    get_redis_connector().delete(
        redis_cabinet_key.format(user.user_id)
    )
