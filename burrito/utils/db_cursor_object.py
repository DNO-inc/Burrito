from peewee import MySQLDatabase
from playhouse.shortcuts import ReconnectMixin

from burrito.utils.singleton_pattern import singleton
from burrito.utils.config_reader import get_config


@singleton
class BurritoDatabaseCursor(ReconnectMixin, MySQLDatabase):
    def __init__(self, database, **kwargs) -> None:
        super().__init__(database, **kwargs)
        self.execute_sql("SET NAMES utf8mb4;")


def get_database_cursor() -> BurritoDatabaseCursor:
    """_summary_

    Create data base cursor

    Returns:
        BurritoDatabaseCursor: current database cursor
    """

    return BurritoDatabaseCursor(
        get_config().BURRITO_DB_NAME,
        user=get_config().BURRITO_DB_USER,
        password=get_config().BURRITO_DB_PASSWORD,
        host=get_config().BURRITO_DB_HOST,
        port=int(get_config().BURRITO_DB_PORT),
        charset="utf8mb4"
    )
