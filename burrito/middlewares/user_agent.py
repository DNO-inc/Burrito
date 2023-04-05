from typing import Any
import re

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from burrito.utils.logger import get_logger


class UserAgentMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            restrict: list[str] = [],
    ):
        super().__init__(app)
        self._restrict = restrict

    async def dispatch(self, request: Request, call_next: Any) -> Any:
        user_agent = request.headers.get('User-Agent')

        if not user_agent:
            return JSONResponse(
                {"detail": "hello bot"},
                status_code=403
            )

        for item in self._restrict:
            if re.match(f"^{item}", user_agent):
                get_logger().warning(f"Bot User-Agent found {user_agent}")

                return JSONResponse(
                    {"detail": "hello bot"},
                    status_code=403
                )

        return await call_next(request)
