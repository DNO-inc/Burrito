import os
import time

from peewee import MySQLDatabase

from burrito.models.m_email_code import EmailVerificationCode
from burrito.models.m_password_rest_model import AccessRenewMetaData
from burrito.plugins.loader import PluginLoader
from burrito.utils.db_cursor_object import get_database_cursor
from burrito.utils.db_utils import create_tables
from burrito.utils.logger import get_logger
from burrito.utils.tasks.preprocessor import preprocessor_task

PluginLoader.load()

if __name__ == "__main__":
    create_tables()
    preprocessor_task()

    from .core import start_scheduler
    from burrito import CURRENT_TIME_ZONE
    from burrito.utils.mongo_util import mongo_init_ttl_indexes
    from burrito.utils.tasks.new_tickets import check_for_new_tickets

    check_for_new_tickets()
    mongo_init_ttl_indexes([EmailVerificationCode, AccessRenewMetaData])

    os.environ['TZ'] = str(CURRENT_TIME_ZONE)
    time.tzset()

    with open("event_init.sql", "r", encoding="utf-8") as file:
        db: MySQLDatabase = get_database_cursor()

        for query in file.read().split(";"):
            query = query.replace('\t', "").replace("\n", "")
            query = ' '.join(query.split())

            if not query:
                continue

            try:
                db.execute_sql(query)
            except Exception as e:
                get_logger().error(e)

    start_scheduler()
