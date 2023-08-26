from pathlib import Path
import inspect


def get_current_app_name() -> str:
    return Path(inspect.getouterframes(inspect.currentframe(), 2)[1][1]).parent.name
