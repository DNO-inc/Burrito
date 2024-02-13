from typing import Any, Literal
import jwt
import uuid

from fastapi import HTTPException, Request, status
from pydantic import BaseModel

from burrito.utils.date import get_timestamp_now
from burrito.utils.logger import get_logger
from burrito.utils.config_reader import get_config
from burrito.utils.redis_utils import get_redis_connector


_JWT_SECRET = get_config().BURRITO_JWT_SECRET
JWT_ACCESS_TTL = int(get_config().BURRITO_JWT_ACCESS_TTL)
JWT_REFRESH_TTL = int(get_config().BURRITO_JWT_REFRESH_TTL)


class AuthTokenError(HTTPException):
    ...


class AuthTokenPayload(BaseModel):
    # common payload
    iss: str = "https://github.com/DNO-inc"
    sub: str = "auth"
    exp: int = 0
    iat: int = 0
    jti: str = ""

    # burrito payload
    user_id: int
    role: str


def _make_redis_key(data: AuthTokenPayload) -> str:
    """This function gets some information from the AuthTokenPayload object and returns the key used to get tokens from redis

    Args:
        data (AuthTokenPayload): token payload

    Returns:
        str: redis key to get access/refresh token
    """
    return "{}_{}".format(
        data.user_id,
        data.jti
    )


def _make_token_body(token_data: AuthTokenPayload, token_type: Literal["access", "refresh"]) -> str:
    """Generate tokens

    Args:
        token_data (AuthTokenPayload): _description_
        token_type (str): type of token, might be access or refresh
        jti (str): token ID, both of tokens have the same jti

    Returns:
        str: access or refresh token
    """

    token_creation_time = get_timestamp_now()

    token_data.jti = uuid.uuid4().hex
    token_data.exp = token_creation_time + (JWT_ACCESS_TTL if token_type == "access" else JWT_REFRESH_TTL)
    token_data.iat = token_creation_time

    return jwt.encode(token_data.dict(), _JWT_SECRET)


def read_token_payload(token: str) -> AuthTokenPayload | None:
    """
    Read the token payload.

    Args:
        token: The token to be read. This should be a JSON Web Token ( JWT )

    Returns:
        The payload or None if the token is invalid or expired
    """

    try:
        return AuthTokenPayload(**jwt.decode(token, _JWT_SECRET, algorithms="HS256"))

    except jwt.exceptions.ExpiredSignatureError as exc:
        raise AuthTokenError(
            detail="Authorization token is expired",
            status_code=status.HTTP_401_UNAUTHORIZED
        ) from exc

    except Exception as exc:
        get_logger().warning("Failed to read token: {token}", exc_info=True)
        raise AuthTokenError(
            detail="Authorization token payload is invalid",
            status_code=status.HTTP_401_UNAUTHORIZED
        ) from exc


def create_access_token(token_data: AuthTokenPayload) -> str:
    return _make_token_body(token_data, "access")


def create_refresh_token(token_data: AuthTokenPayload) -> str:
    _token = _make_token_body(token_data, "refresh")
    _token_redis_key = _make_redis_key(token_data)

    get_redis_connector().set(_token_redis_key, _token)
    get_redis_connector().expire(_token_redis_key, JWT_REFRESH_TTL)
    get_logger().info(
        f"""
            Generate new token:
                * token: {_token}
                * redis key: {_token_redis_key}
                * payload:  {token_data.dict()}

        """
    )
    return _token


class BurritoJWT:
    def __init__(self, request: Request = None) -> None:
        """
        Initialize the object.

        Args:
            request: The request object that will be used to extract token from authorization header
        """

        self.__req = request
        self.__token = self._get_clear_token()

    def __call__(self) -> Any:
        pass

    def _get_clear_token(self) -> str:
        """
        Get clear token from authorization header.

        Returns:
            Clear token or None if not present in the header
        """

        raw_token = self.__req.headers.get("authorization")

        if not raw_token:
            return None

        return raw_token.removeprefix("Bearer ")

    @property
    def request(self) -> Request:
        return self.__req

    async def create_token_pare(self, token_data: AuthTokenPayload) -> dict[str, str]:
        """
        Create a tokens pare (access and refresh)

        Args:
            token_data: The payload of the token

        Returns:
            A dictionary containing the access and refresh tokens
        """

        return {
            "access_token": create_access_token(token_data),
            "refresh_token": create_refresh_token(token_data)
        }

    async def require_access_token(self) -> AuthTokenPayload:
        """
        Check if access token is valid.

        Returns:
            An auth token payload or None if token is invalid.
        """

        # Raise an AuthTokenError if the token is not valid.
        if not self.__token:
            raise AuthTokenError(
                detail="Missing authorization header",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        return read_token_payload(self.__token)

    async def require_refresh_token(self) -> AuthTokenPayload:
        """
        Check if refresh token is valid.

        Returns:
            An auth token payload or None if token is invalid.
        """

        # Raise an AuthTokenError if the token is not valid.
        if not self.__token:
            raise AuthTokenError(
                detail="Missing authorization header",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        token_payload = read_token_payload(self.__token)

        stored_token = get_redis_connector().get(_make_redis_key(token_payload))
        if not stored_token:
            raise AuthTokenError(
                detail="Authorization error: refresh token is invalid or expired",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        if (stored_token.decode("utf-8") != self.__token):
            get_logger().error(
                f"""
                    refresh token is invalid or expired:
                        * payload:  {token_payload.dict()}

                """
            )
            raise AuthTokenError(
                detail="Authorization error: refresh token is invalid or expired",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        return token_payload

    async def rotate_refresh_token(self) -> str:
        token_payload = await self.require_refresh_token()

        get_redis_connector().delete(_make_redis_key(token_payload))

        return create_refresh_token(token_payload)

    async def delete_refresh_token(self):
        """
        Delete refresh token from database.
        """

        get_redis_connector().delete(_make_redis_key(await self.require_refresh_token()))


def get_auth_core() -> BurritoJWT:
    """
    Provides access to Burrito's auth system.
    It is used to authenticate a user and get the token that is associated with that user.
    """

    return BurritoJWT
