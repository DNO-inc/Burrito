from burrito.schemas.pagination_schema import BurritoPagination


class BaseFilterSchema(BurritoPagination):
    anonymous: bool | None
    faculty: int | None
    status: list[int] | None
    scope: str | None
    queue: list[int] | None
