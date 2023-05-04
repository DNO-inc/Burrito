
from fastapi import status

__all__ = ("status", "BaseView")


class BaseView:
    _permissions: list[str] = []
