import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from burrito.apps.registration.router import registration_router
from burrito.apps.about.router import about_router

from burrito.apps.auth.router import auth_router
from burrito.apps.profile.router import profile_router

from burrito.apps.reports.router import reports_router

from burrito.utils.db_utils import create_tables
from burrito.utils.app_util import connect_app
from burrito.utils.db_backup_util import backup_cycle
from burrito.utils.task_manager import get_async_manager
from burrito.utils.logger import logger

create_tables()

app = FastAPI()
connect_app(app, "/about", about_router)
connect_app(app, "/registration", registration_router)
connect_app(app, "/profile", profile_router)
connect_app(app, "/auth", auth_router)
connect_app(app, "/reports", reports_router)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.on_event("startup")
async def startup_event():
    """Setup task when when server is started"""

    task_manager = get_async_manager()
    task_manager.add_task(backup_cycle())
    task_manager.run()

    logger.info("All tasks was started")


if __name__ == "__main__":
    uvicorn.run("burrito.__main__:app", port=8080, reload=True)
