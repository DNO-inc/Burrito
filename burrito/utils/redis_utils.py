import redis
from fastapi import HTTPException

from burrito.utils.singleton_pattern import singleton
from burrito.utils.config_reader import get_config
from burrito.utils.logger import get_logger


@singleton
class RedisConnector(redis.Redis):
    def __init__(self, *, host: str, port: int, password: str | None = None, **kwargs):
        """
        Initialize connection to server.

        Args:
            host: domain name or IP address
            port: Port number to connect to
            password: Password to use for authentication
        """
        super().__init__(host=host, port=port, password=password, **kwargs)


def get_redis_connector() -> RedisConnector:
    """
    Returns redis connector to interact with Redis database.
    """
    _redis_object = RedisConnector(
        host=get_config().BURRITO_REDIS_HOST,
        port=int(get_config().BURRITO_REDIS_PORT)
    )

    try:
        _redis_object.ping()
    except (redis.exceptions.ConnectionError, ConnectionRefusedError) as exc:
        get_logger().critical("Redis server is unavailable")
        raise HTTPException(
            status_code=500,
            detail="Some of the services is unavailable, please try late"
        ) from exc

    return _redis_object
