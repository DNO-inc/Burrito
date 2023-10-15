import time
import os

from burrito import CURRENT_TIME_ZONE
from burrito.plugins.loader import PluginLoader

from .core import start_scheduler


if __name__ == "__main__":
    PluginLoader.load()

    os.environ['TZ'] = str(CURRENT_TIME_ZONE)
    time.tzset()

    start_scheduler()
