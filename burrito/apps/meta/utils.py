from typing import Any

from pydantic import BaseModel


class RolesResponse(BaseModel):
    role_id: int
    name: str
    priority: int


class RolePermissionResponse(BaseModel):
    role: Any
    permission: Any
