from cachetools import TTLCache

from .singleton_pattern import singleton


@singleton
class BurritoCache(TTLCache):
    def __init__(self, *, maxsize: int = 2024, ttl: float = 3036):
        super().__init__(
            maxsize=maxsize,
            ttl=ttl
        )


def get_ttl_cache_core():
    return BurritoCache()
