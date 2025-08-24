from typing import Optional

from burrito.schemas.pagination_schema import BurritoPagination


class BaseFilterSchema(BurritoPagination):
    anonymous: Optional[bool] = None
    faculty: Optional[int] = None
    status: Optional[list[int]] = None
    scope: Optional[str] = None
    queue: Optional[list[int]] = None
