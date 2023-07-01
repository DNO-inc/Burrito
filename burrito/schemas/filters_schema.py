from burrito.schemas.pagination_schema import BurritoPagination


class BaseFilterSchema(BurritoPagination):
    anonymous: bool | None
    faculty: int | None
    queue: int | None
    status: list[int] | None
