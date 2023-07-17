import redis

from burrito.utils.singleton_pattern import singleton
from burrito.utils.config_reader import get_config


@singleton
class RedisConnector(redis.Redis):
    def __init__(self, *, host: str, port: int, password: str | None = None, **kwargs):
        super().__init__(host=host, port=port, password=password, **kwargs)


def get_redis_connector() -> RedisConnector:
    return RedisConnector(
        host=get_config().BURRITO_REDIS_HOST,
        port=int(get_config().BURRITO_REDIS_PORT)
    )
