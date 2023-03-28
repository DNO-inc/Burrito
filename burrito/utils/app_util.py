from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from burrito.utils.singleton_pattern import singleton
from burrito.utils.db_backup_util import backup_cycle
from burrito.utils.task_manager import get_async_manager
from burrito.utils.logger import logger


@singleton
class BurritoApi(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


def get_current_app():
    """Return current application object"""

    app = BurritoApi()

    app.add_event_handler("startup", startup_event)
    app.add_exception_handler(AuthJWTException, authjwt_exception_handler)

    return app


async def startup_event():
    """Setup task when when server is started"""

    task_manager = get_async_manager()
    task_manager.add_task(backup_cycle())
    task_manager.run()

    logger.info("All tasks was started")


async def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


def connect_app(fast_api_object: FastAPI, prefix: str, router: APIRouter):
    """Connect fastapi routers to main app"""

    fast_api_object.include_router(router=router, prefix=prefix)
