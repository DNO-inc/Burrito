from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from burrito.utils.singleton_pattern import singleton
from burrito.utils.db_backup_util import backup_cycle
from burrito.utils.task_manager import get_async_manager
from burrito.utils.logger import get_logger


@singleton
class BurritoApi(FastAPI):
    """_summary_

    Main application object
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


def get_current_app() -> BurritoApi:
    """_summary_

    Return current application object

    Returns:
        BurritoApi: current application object
    """

    app = BurritoApi()

    app.add_event_handler("startup", startup_event)
    app.add_exception_handler(AuthJWTException, authjwt_exception_handler)

    return app


async def startup_event():
    """_summary_

    Setup task when when server is started
    """

    task_manager = get_async_manager()
    task_manager.add_task(backup_cycle())
    task_manager.run()

    get_logger().info("All tasks was started")


async def authjwt_exception_handler(request: Request, exc: AuthJWTException) -> JSONResponse:
    """_summary_

    Args:
        request (Request): request object
        exc (AuthJWTException): exception type

    Returns:
        JSONResponse: json response that user will recv
    """

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


def connect_app(fast_api_object: FastAPI, prefix: str, router: APIRouter):
    """_summary_

        Args:
        fast_api_object (FastAPI): main FastApi router
        prefix (str): app url
        router (APIRouter): application router
    """

    fast_api_object.include_router(router=router, prefix=prefix)
