from typing import Any, Literal, Dict
import jwt
import uuid

from fastapi import HTTPException, Request, status
from pydantic import BaseModel

from burrito.utils.date import get_timestamp_now
from burrito.utils.logger import get_logger
from burrito.utils.config_reader import get_config
from burrito.utils.redis_utils import get_redis_connector
from burrito.utils.users_util import get_user_by_id
from burrito.utils.permissions_checker import check_permission

from burrito.models.user_model import Users

_JWT_SECRET = get_config().BURRITO_JWT_SECRET
JWT_ACCESS_TTL = int(get_config().BURRITO_JWT_ACCESS_TTL)
JWT_REFRESH_TTL = int(get_config().BURRITO_JWT_REFRESH_TTL)


class AuthTokenError(HTTPException):
    ...


class AuthTokenPayload(BaseModel):
    """
    Attributes:
        iss         token issuer
        sub         subject of JWT
        exp         expiration time (UNIX timestamp)
        iat         time at which the token was created (UNIX timestamp)
        jti         token ID
        user_id     current user ID
        role        role name of the current user (only used on fronted)
    """

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
    return f"{data.user_id}_{data.jti}"


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
    """
    Returns access JWT.

    Args:
        token_data (AuthTokenPayload): JWT payload

    Returns:
        str: access token
    """

    return _make_token_body(token_data, "access")


def create_refresh_token(token_data: AuthTokenPayload) -> str:
    """
    Returns refresh JWT and store it in Redis storage for further validation.

    Args:
        token_data (AuthTokenPayload): JWT payload

    Returns:
        str: refresh token
    """

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


def create_token_pare(token_data: AuthTokenPayload) -> Dict[str, str]:
    """Creates both of tokens access and refresh.

    Args:
        token_data (AuthTokenPayload): JWT payload

    Returns:
        dict[str, str]: access and refresh tokens
    """

    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data)
    }


def _extract_from_headers(headers: Dict[str, Any]) -> str:
    """Get request headers and extract JWT from authorization header

    Args:
        headers (Dict[str, Any]): request headers

    Raises:
        AuthTokenError: Raised if Authorization header is not provided

    Returns:
        str: pure JWT token without the 'Bearer' prefix
    """

    raw_token = headers.get("authorization")
    if not raw_token:
        raise AuthTokenError(
            detail="Missing authorization header",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return raw_token.removeprefix("Bearer ")


def _require_refresh_token(headers: Dict[str, Any]) -> AuthTokenPayload:
    """Try to extract and validate refresh JWT.

    Args:
        headers (Dict[str, Any]): request headers

    Raises:
        AuthTokenError: Raised if Authorization header is not provided or token is expired

    Returns:
        AuthTokenPayload: JWT payload
    """

    raw_token = _extract_from_headers(headers)
    token_payload = read_token_payload(raw_token)

    stored_token = get_redis_connector().get(_make_redis_key(token_payload))
    if not stored_token:
        raise AuthTokenError(
            detail="Authorization error: refresh token is invalid or expired",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    if (stored_token.decode("utf-8") != raw_token):
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


class get_current_user:
    """
    Dependency to determine the current user
    """

    def __init__(self, permission_list: set[tuple] | None = None) -> None:
        self._permission_list = permission_list

    def __call__(self, request: Request) -> Users:
        """
        Args:
            request (Request): request object for extraction authorization headers

        Returns:
            Users: current user, the owner of the given token
        """
        current_user = get_user_by_id(
            read_token_payload(_extract_from_headers(request.headers)).user_id
        )
        check_permission(current_user, self._permission_list)

        return current_user


def rotate_refresh_token(request: Request) -> str:
    """
    Extracts refresh token from headers and refresh it

    Args:
        request (Request): request object for extraction authorization headers

    Returns:
        str: new refresh token
    """
    token_payload = _require_refresh_token(request.headers)

    current_user = get_user_by_id(token_payload.user_id)

    get_redis_connector().delete(_make_redis_key(token_payload))

    return current_user, create_refresh_token(token_payload)


def delete_refresh_token(request: Request):
    """
    Delete refresh token

    Args:
        request (Request): request object for extraction authorization headers
    """

    token_payload = _require_refresh_token(request.headers)

    current_user = get_user_by_id(token_payload.user_id)

    get_redis_connector().delete(
        _make_redis_key(token_payload)
    )

    return current_user
