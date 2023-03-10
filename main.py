
from fastapi import FastAPI

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from apps.about.router import about_router
from apps.registration.router import registration_router
from apps.auth.router import auth_router
from apps.account.router import account_router

from utils.db_utils import create_tables
from utils.app_util import connect_app



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




# D.N.O


