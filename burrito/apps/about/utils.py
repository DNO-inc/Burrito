from pathlib import Path
from functools import cache

from burrito.utils.logger import get_logger


def read_file(path_to_file: str):
    if not Path.exists(path_to_file):
        get_logger().critical(f"{path_to_file} file is not exist")
        return ""

    data = ""
    with open(path_to_file, encoding="utf-8") as file:
        while True:
            line = file.readline()

            if not line:
                break

            data += line
            line = ""

    return data


@cache
def get_changelog() -> str:
    return read_file(Path(__file__).parents[3] / "CHANGELOG.md")


@cache
def get_contributors() -> str:
    return read_file(Path(__file__).parents[3] / "CONTRIBUTORS.md")
