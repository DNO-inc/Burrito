from typing import Any
import jwt
import uuid

from fastapi import HTTPException, Request, status
from pydantic import BaseModel

from burrito.utils.config_reader import get_config
from burrito.utils.redis_utils import get_redis_connector


class AuthTokenError(HTTPException):
    ...


class AuthTokenPayload(BaseModel):
    token_id: str = ""
    token_type: str = ""
    user_id: int
    role: str


_JWT_SECRET = get_config().BURRITO_JWT_SECRET
_TOKEN_TTL = get_config().BURRITO_JWT_TTL
_KEY_TEMPLATE = "{}_{}_{}"


def _make_redis_key(data: AuthTokenPayload) -> str:
    return _KEY_TEMPLATE.format(
        data.token_id,
        data.token_type,
        data.user_id
    )


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

    async def create_access_token(self, token_data: AuthTokenPayload) -> str:
        token_data.token_id = uuid.uuid4().hex
        token_data.token_type = "access"

        _token = jwt.encode(token_data.dict(), _JWT_SECRET).decode("utf-8")
        _token_redis_key = _make_redis_key(token_data)

        get_redis_connector().set(_token_redis_key, _token)
        get_redis_connector().expire(_token_redis_key, _TOKEN_TTL)
        return _token

    async def create_refresh_token(self, token_data: AuthTokenPayload) -> str:
        token_data.token_id = uuid.uuid4().hex
        token_data.token_type = "refresh"

        _token = jwt.encode(token_data.dict(), _JWT_SECRET).decode("utf-8")
        _token_redis_key = _make_redis_key(token_data)

        get_redis_connector().set(_token_redis_key, _token)
        get_redis_connector().expire(_token_redis_key, _TOKEN_TTL)
        return _token

    async def create_token_pare(self, token_data: AuthTokenPayload) -> dict[str, str]:
        return {
            "access_token": await self.create_access_token(token_data),
            "refresh_token": await self.create_refresh_token(token_data)
        }

    async def verify_access_token(self) -> AuthTokenPayload:
        if not self.__token:
            raise AuthTokenError(
                detail="Missing authorization header",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        token_payload = await self._read_token_payload(self.__token)
        token_key = _make_redis_key(token_payload)

        if get_redis_connector().get(token_key):
            return token_payload

        raise AuthTokenError(
            detail="Authorization token is invalid or expired",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    async def verify_refresh_token(self) -> AuthTokenPayload:
        if not self.__token:
            raise AuthTokenError(
                detail="Missing authorization header",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        token_payload = await self._read_token_payload(self.__token)
        token_key = _make_redis_key(token_payload)

        if get_redis_connector().get(token_key):
            return token_payload

        raise AuthTokenError(
            detail="Authorization token is invalid or expired",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    async def _read_token_payload(self, token: str) -> AuthTokenPayload | None:
        try:
            return AuthTokenPayload(**jwt.decode(token, _JWT_SECRET))
        except:
            raise AuthTokenError(
                detail="Authorization token is invalid or expired",
                status_code=status.HTTP_401_UNAUTHORIZED
            )


def get_auth_core() -> BurritoJWT:
    return BurritoJWT
