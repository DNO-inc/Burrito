from typing import Any

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from burrito.utils.auth import AuthTokenError
from burrito.utils.logger import get_logger
from burrito.utils.auth import (
    _read_token_payload, _make_redis_key, AuthTokenPayload
)
from burrito.utils.redis_utils import get_redis_connector


EXCLUDE_APPS: tuple = ("anon", "meta", "about", "registration")
EXCLUDE_URI: dict = {
    "auth": ("/password/login")
}
INSTALLED_APPS = (
    "about",
    "registration",
    "profile",
    "auth",
    "tickets",
    "admin",
    "anon",
    "meta",
    "comments",
    "notifications"
)


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Any) -> Any:
        try:
            raw_data = request.url.path.split("/")
            app_name = raw_data[1]

            if app_name not in INSTALLED_APPS or app_name in EXCLUDE_APPS:
                return await call_next(request)

            app_uri = f"/{'/'.join(raw_data[2:])}"

            exclude_uri_list = EXCLUDE_URI.get(app_name)
            if exclude_uri_list and app_uri in exclude_uri_list:
                return await call_next(request)

            raw_token = request.headers.get("authorization")
            if not raw_token:
                return JSONResponse(
                    content={"detail": "Missing authorization header"},
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )

            raw_token = raw_token.removeprefix("Bearer ")

            token_payload: AuthTokenPayload = _read_token_payload(raw_token)

            token_key = _make_redis_key(token_payload)
            if get_redis_connector().get(token_key).decode("utf-8") == raw_token:
                return await call_next(request)

            get_logger().error(
                f"""
                    Authorization error:
                        * token: {raw_token}
                        * redis key: {token_key}
                        * payload:  {token_payload.dict()}

                """
            )
            return JSONResponse(
                content={"detail": "Authorization token is invalid or expired -_-"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        except AuthTokenError as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail}
            )
