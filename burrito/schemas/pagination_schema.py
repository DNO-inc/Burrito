from pydantic import BaseModel, validator


class BurritoPagination(BaseModel):
    start_page: int = 1
    tickets_count: int = 10

    @validator("start_page", "tickets_count")
    @classmethod
    def is_valid_num(cls, value: int) -> int | None:
        if value <= 0:
            raise ValueError("Value should be more than 0")

        return value
