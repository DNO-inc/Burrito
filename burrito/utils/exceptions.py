from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from burrito.utils.logger import get_logger


class DBConnectionError(HTTPException):
    def __init__(self, detail: str = "One of dbs is unreachable") -> None:
        super().__init__(500, detail)

    def __str__(self) -> str:
        return super().__repr__()


class MySQLConnectionError(DBConnectionError):
    def __init__(self, detail: str = "Can't connect to MySQL") -> None:
        super().__init__(detail)


class RedisConnectionError(DBConnectionError):
    def __init__(self, detail: str = "Can't connect to Redis") -> None:
        super().__init__(detail)


class MongoConnectionError(DBConnectionError):
    def __init__(self, detail: str = "Can't connect to Mongo") -> None:
        super().__init__(detail)


def db_connection_error_handler(request, exc) -> JSONResponse:
    get_logger().critical(str(exc))
    return JSONResponse(
        content={"detail": "Some internal services is unreachable"},
        status_code=500
    )
