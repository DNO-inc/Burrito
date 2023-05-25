import os
import re
from collections import OrderedDict

from dotenv import dotenv_values, find_dotenv

from burrito.utils.singleton_pattern import singleton
from burrito.utils.logger import get_logger


@singleton
class EnvConfigReader:
    def __init__(self, base_word: str = "BURRITO_") -> None:
        self.__pattern = re.compile(fr"{base_word}\w+")
        self.__config: dict[str, str] | OrderedDict[str, str] = {}

        self._read()

    def _read(self) -> None:
        __env_path = find_dotenv()
        if __env_path:
            self.__config = dotenv_values(__env_path)
            get_logger().info(f".env file is found ({__env_path})")

        for key, value in os.environ.items():
            if re.match(self.__pattern, key):
                self.__config[key] = value

    def __getattr__(self, __name: str) -> int | str | None:
        _value = self.__config.get(__name)

        if _value is None:
            get_logger().warning(f"Environment variable {__name} is undefined")
            get_logger().info(f"Loaded variables: {list(self.__config)}")

        return _value

    @property
    def config(self) -> dict[str, str] | OrderedDict[str, str]:
        return self.__config


def get_config() -> EnvConfigReader:
    return EnvConfigReader()
