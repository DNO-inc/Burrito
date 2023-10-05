import time
import os

from burrito import CURRENT_TIME_ZONE

from .core import start_scheduler


os.environ['TZ'] = str(CURRENT_TIME_ZONE)
time.tzset()

start_scheduler()
