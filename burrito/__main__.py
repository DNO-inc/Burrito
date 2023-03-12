
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from burrito.apps.registration.router import registration_router
from burrito.apps.about.router import about_router

from burrito.apps.auth.router import auth_router
from burrito.apps.account.router import account_router

from burrito.utils.db_utils import create_tables
from burrito.utils.app_util import connect_app

create_tables()

app = FastAPI()
connect_app(app, "/about", about_router)
connect_app(app, "/registration", registration_router)
connect_app(app, "/account", account_router)
connect_app(app, "/auth", auth_router)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


if __name__ == "__main__":
    uvicorn.run("burrito.__main__:app", port=8080, reload=True)
