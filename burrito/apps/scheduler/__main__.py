import time
import os

from burrito.models.m_email_code import EmailVerificationCode

from burrito.utils.db_utils import create_tables
from burrito.utils.tasks.preprocessor import preprocessor_task
from burrito.utils.mongo_util import mongo_init_ttl_indexes

from burrito.plugins.loader import PluginLoader


PluginLoader.load()

if __name__ == "__main__":
    create_tables()
    preprocessor_task()
    mongo_init_ttl_indexes([EmailVerificationCode])

    from burrito import CURRENT_TIME_ZONE

    from .core import start_scheduler

    os.environ['TZ'] = str(CURRENT_TIME_ZONE)
    time.tzset()

    start_scheduler()
