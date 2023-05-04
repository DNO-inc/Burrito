from pydantic import BaseModel


class ResponseCode(BaseModel):
    SUCCESSFUL: int = 200
    CREATED: int = 201

    UNAUTHORIZED: int = 401
    ACCESS_FORBIDDEN: int = 403
    NOT_FOUNT: int = 404
    CONFLICT: int = 409
    UNSUPPORTED_MEDIA_TYPE: int = 415
    LOCKED: int = 423
    TOO_MANY_REQUESTS: int = 429

    WTF_ERROR: int = 500
    NOT_IMPLEMENTED: int = 501
    SERVICE_UNAVAILABLE: int = 503
