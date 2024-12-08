import inspect
from pathlib import Path

from uvicorn.config import LOGGING_CONFIG

LOGGING_CONFIG["formatters"]["default"]["fmt"] = "[ %(asctime)s ] | %(name)s (%(process)d) | %(levelprefix)s %(message)s"
LOGGING_CONFIG["formatters"]["access"]["fmt"] = "[ %(asctime)s ] | %(name)s (%(process)d) | %(levelprefix)s %(client_addr)s - \"%(request_line)s\" %(status_code)s"


def get_current_app_name() -> str:
    return Path(inspect.getouterframes(inspect.currentframe(), 2)[1][1]).parent.name
