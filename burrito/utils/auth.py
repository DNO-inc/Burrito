from typing import Any
from datetime import datetime
import jwt
import uuid

from fastapi import HTTPException, Request, status
from pydantic import BaseModel

from burrito.utils.logger import get_logger
from burrito.utils.config_reader import get_config
from burrito.utils.redis_utils import get_redis_connector


_JWT_SECRET = get_config().BURRITO_JWT_SECRET
_TOKEN_TTL = int(get_config().BURRITO_JWT_TTL)
_KEY_TEMPLATE = "{}_{}_{}"
_TOKEN_TYPES = {"access", "refresh"}


class AuthTokenError(HTTPException):
    ...


class AuthTokenPayload(BaseModel):
    # common payload
    iss: str = "DNO-inc"
    sub: str = "auth"
    exp: float = 0
    iat: float = 0
    jti: str = ""

    # burrito payload
    token_type: str = ""
    user_id: int
    role: str


def _make_redis_key(data: AuthTokenPayload) -> str:
    return _KEY_TEMPLATE.format(
        data.jti,
        data.token_type,
        data.user_id
    )


def _make_token_body(token_data: AuthTokenPayload, token_type: str) -> str:
    token_creation_time = datetime.now().timestamp()

    token_data.jti = uuid.uuid4().hex
    token_data.token_type = token_type
    token_data.exp = token_creation_time + _TOKEN_TTL
    token_data.iat = token_creation_time

    return jwt.encode(token_data.dict(), _JWT_SECRET).decode("utf-8")


def _read_token_payload(token: str) -> AuthTokenPayload | None:
    try:
        return AuthTokenPayload(**jwt.decode(token, _JWT_SECRET))

    except jwt.exceptions.ExpiredSignatureError as exc:
        raise AuthTokenError(
            detail="Authorization token is expired",
            status_code=status.HTTP_401_UNAUTHORIZED
        ) from exc

    except Exception as exc:
        raise AuthTokenError(
            detail="Authorization token payload is invalid",
            status_code=status.HTTP_401_UNAUTHORIZED
        ) from exc


class BurritoJWT:
    def __init__(self, request: Request = None) -> None:
        self.__req = request
        self.__token = self._get_clear_token()

    def __call__(self) -> Any:
        pass

    def _get_clear_token(self) -> str:
        raw_token = self.__req.headers.get("authorization")

        if not raw_token:
            return None

        return raw_token.removeprefix("Bearer ")

    @property
    def request(self) -> Request:
        return self.__req

    async def push_token(self, token_data: AuthTokenPayload, token_type: str) -> str:
        if token_type not in _TOKEN_TYPES:
            raise AuthTokenError(
                detail=f"Invalid token type: available token types is {_TOKEN_TYPES}, received {token_type}",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        _token = _make_token_body(token_data, token_type)
        _token_redis_key = _make_redis_key(token_data)

        get_redis_connector().set(_token_redis_key, _token)
        get_redis_connector().expire(_token_redis_key, _TOKEN_TTL)
        return _token

    async def create_token_pare(self, token_data: AuthTokenPayload) -> dict[str, str]:
        return {
            "access_token": await self.push_token(token_data, "access"),
            "refresh_token": await self.push_token(token_data, "refresh")
        }

    async def verify_token(self) -> AuthTokenPayload:
        """
            This function verify current token received from user in headers, it can be access or refresh token.

        """

        if not self.__token:
            raise AuthTokenError(
                detail="Missing authorization header",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        token_payload = _read_token_payload(self.__token)
        token_key = _make_redis_key(token_payload)

        if get_redis_connector().get(token_key):
            return token_payload

        get_logger().error(f"Authorization: something went wrong with token payload {token_payload.dict()}")
        raise AuthTokenError(
            detail="Authorization error: something went wrong",
            status_code=status.HTTP_401_UNAUTHORIZED
        )


def get_auth_core() -> BurritoJWT:
    return BurritoJWT
