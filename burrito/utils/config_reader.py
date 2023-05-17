import os
import re

from burrito.utils.singleton_pattern import singleton


@singleton
class EnvConfigReader:
    def __init__(self, base_word: str = "BURRITO_") -> None:
        self.__pattern = re.compile(fr"{base_word}\w+")
        self.__config: dict[str, str] = {}

        self._read()

    def _read(self) -> None:
        for key, value in os.environ.items():
            if re.match(self.__pattern, key):
                self.__config[key] = value

    def __getattr__(self, __name: str) -> int | str | None:
        return self.__config.get(__name)

    @property
    def config(self):
        return self.__config


def get_config():
    return EnvConfigReader()
