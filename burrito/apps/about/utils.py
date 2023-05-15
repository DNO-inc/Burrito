from pathlib import Path
from cachetools import cached

from burrito.utils.cache_util import BurritoCache
from burrito.utils.logger import get_logger


def read_file(path_to_file: str) -> str:
    """_summary_

    Return file content if file exist else return empty string

    Args:
        path_to_file (str): path to file to read it

    Returns:
        str: file content
    """

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


@cached(BurritoCache())
def get_changelog() -> str:
    """_summary_

    Returns:
        str: changelog data in Markdown format
    """

    return read_file(Path(__file__).parents[3] / "CHANGELOG.md")


@cached(BurritoCache())
def get_contributors() -> str:
    """_summary_

    Returns:
        str: contributors information in Markdown format
    """

    return read_file(Path(__file__).parents[3] / "CONTRIBUTORS.md")
