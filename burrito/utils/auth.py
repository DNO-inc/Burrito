from copy import deepcopy
from typing import Any, Literal
import secrets
import jwt
import uuid

from fastapi import HTTPException, Request, status
from pydantic import BaseModel

from burrito.utils.date import get_timestamp_now
from burrito.utils.logger import get_logger
from burrito.utils.config_reader import get_config
from burrito.utils.redis_utils import get_redis_connector


_JWT_SECRET = get_config().BURRITO_JWT_SECRET
_JWT_ACCESS_TTL = int(get_config().BURRITO_JWT_ACCESS_TTL)
_JWT_REFRESH_TTL = int(get_config().BURRITO_JWT_REFRESH_TTL)
_KEY_TEMPLATE = "{}_{}_{}"
_TOKEN_TYPES = {"access", "refresh"}


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
    token_type: str = ""
    user_id: int
    role: str
    burrito_salt: str = ""


def _make_redis_key(data: AuthTokenPayload) -> str:
    """This function gets some information from the AuthTokenPayload object and returns the key used to get tokens from redis

    Args:
        data (AuthTokenPayload): token payload

    Returns:
        str: redis key to get access/refresh token
    """

    return _KEY_TEMPLATE.format(
        data.jti,
        data.token_type,
        data.user_id
    )


def _make_token_body(token_data: AuthTokenPayload, token_type: str, jti: str) -> str:
    """Generate tokens

    Args:
        token_data (AuthTokenPayload): _description_
        token_type (str): type of token, might be access or refresh
        jti (str): token ID, both of tokens have the same jti

    Returns:
        str: access or refresh token
    """

    token_creation_time = get_timestamp_now()

    token_data.jti = jti
    token_data.token_type = token_type
    token_data.exp = token_creation_time + (_JWT_ACCESS_TTL if token_type == "access" else _JWT_REFRESH_TTL)
    token_data.iat = token_creation_time
    token_data.burrito_salt = secrets.token_hex(64)

    return jwt.encode(token_data.dict(), _JWT_SECRET).decode("utf-8")


def _read_token_payload(token: str) -> AuthTokenPayload | None:
    """
    Read the token payload.

    Args:
        token: The token to be read. This should be a JSON Web Token ( JWT )

    Returns:
        The payload or None if the token is invalid or expired
    """

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

    async def push_token(self, token_data: AuthTokenPayload, token_type: Literal["access", "refresh"], _jti: str) -> str:
        """
        Store token in Redis. This method is used to store token in Redis.

        Args:
            token_data: AuthTokenPayload with token data.
            token_type: Type of token ( access or refresh )
            _jti: JTI that is used to sign the token

        Returns:
            A token that can be used for authentication with other methods in this API.
        """

        # Raises an AuthTokenError if the token type is not one of the token types.
        if token_type not in _TOKEN_TYPES:
            raise AuthTokenError(
                detail=f"Invalid token type: available token types is {_TOKEN_TYPES}, received {token_type}",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        _token = _make_token_body(token_data, token_type, _jti)
        _token_redis_key = _make_redis_key(token_data)

        get_redis_connector().set(_token_redis_key, _token)
        get_redis_connector().expire(_token_redis_key, (_JWT_ACCESS_TTL if token_type == "access" else _JWT_REFRESH_TTL))
        get_logger().info(
            f"""
                Generate new token:
                    * token: {_token}
                    * redis key: {_token_redis_key}
                    * payload:  {token_data.dict()}

            """
        )
        return _token

    async def create_token_pare(self, token_data: AuthTokenPayload) -> dict[str, str]:
        """
        Create a tokens pare (access and refresh)

        Args:
            token_data: The payload of the token

        Returns:
            A dictionary containing the access and refresh tokens
        """
        jti = uuid.uuid4().hex

        return {
            "access_token": await self.push_token(token_data, "access", jti),
            "refresh_token": await self.push_token(token_data, "refresh", jti)
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

        return check_jwt_token(self.__token)

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

        token_payload = _read_token_payload(self.__token)

        # If the refresh token is invalid or expired raise an AuthTokenError.
        if (
            token_payload.token_type != "refresh" or
            get_redis_connector().get(_make_redis_key(token_payload)).decode("utf-8") != self.__token
        ):
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

    async def refresh_access_token(self) -> str:
        """
        Refreshes the access token.

        Returns:
            The new access token.
        """

        refresh_token_payload = await self.require_refresh_token()

        access_token_old_payload: AuthTokenPayload = deepcopy(refresh_token_payload)
        access_token_old_payload.token_type = "access"
        get_redis_connector().delete(_make_redis_key(access_token_old_payload))

        return await self.push_token(refresh_token_payload, "access", refresh_token_payload.jti)

    async def delete_token_pare(self):
        """
        Delete token pare. This is used to clean up after a user logs out of the application and the token is no longer valid
        """

        refresh_token_payload = await self.require_refresh_token()

        access_token_payload: AuthTokenPayload = deepcopy(refresh_token_payload)
        access_token_payload.token_type = "access"

        get_redis_connector().delete(_make_redis_key(refresh_token_payload))
        get_redis_connector().delete(_make_redis_key(access_token_payload))


def check_jwt_token(token: str) -> AuthTokenPayload | None:
    """
    Check if token is valid and not expired. This is a helper function to check the validity of a JWT token

    Args:
        token: Token received from token endpoint

    Returns:
        Token payload if valid or None if not valid or expired
    """

    token_payload = _read_token_payload(token)

    # Check if the token is valid or expired.
    if (
        token_payload.token_type != "access" or
        get_redis_connector().get(_make_redis_key(token_payload)).decode("utf-8") != token
    ):
        get_logger().error(
            f"""
                access token is invalid or expired:
                    * payload:  {token_payload.dict()}

            """
        )
        raise AuthTokenError(
            detail="Authorization error: access token is invalid or expired",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return token_payload


def get_auth_core() -> BurritoJWT:
    """
    Provides access to Burrito's auth system. It is used to authenticate a user and get the token that is associated with that user.
    """

    return BurritoJWT
