import redis

from burrito.utils.config_reader import get_config
from burrito.utils.exceptions import DBConnectionError, RedisConnectionError
from burrito.utils.singleton_pattern import singleton


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


def get_redis_connector() -> redis.Redis:
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
        raise RedisConnectionError(str(exc)) from exc

    except Exception as exc:
        raise DBConnectionError(str(exc)) from exc

    return _redis_object
