import json

from fastapi import HTTPException, status
from pydantic import BaseModel, ValidationError


class AuthTokenError(HTTPException):
    ...


class AuthTokenPayload(BaseModel):
    user_id: int
    role: str


def create_access_token_payload(token_data: AuthTokenPayload) -> str:
    return json.dumps(token_data.dict())


def read_access_token_payload(token: str) -> AuthTokenPayload | None:
    payload = None
    try:
        payload = AuthTokenPayload(**json.loads(token))
    except ValidationError as error:
        raise AuthTokenError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token is invalid"
        ) from error

    return payload
