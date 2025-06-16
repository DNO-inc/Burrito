from peewee import MySQLDatabase
from playhouse.shortcuts import ReconnectMixin
from pymysql import connect as pymysql_conn
from pymysql.err import OperationalError

from burrito.utils.config_reader import get_config
from burrito.utils.exceptions import DBConnectionError, MySQLConnectionError
from burrito.utils.singleton_pattern import singleton


@singleton
class BurritoDatabaseCursor(ReconnectMixin, MySQLDatabase):
    def __init__(self, database, **kwargs) -> None:
        temp_conn = pymysql_conn(**kwargs)
        temp_conn.cursor().execute(f"CREATE DATABASE IF NOT EXISTS {get_config().BURRITO_DB_NAME};")
        temp_conn.close()

        super().__init__(database, **kwargs)
        self.execute_sql("SET NAMES utf8mb4;")


def get_database_cursor() -> BurritoDatabaseCursor:
    """
    Create data base cursor

    Returns:
        BurritoDatabaseCursor: current database cursor
    """

    try:
        return BurritoDatabaseCursor(
            get_config().BURRITO_DB_NAME,
            user=get_config().BURRITO_DB_USER,
            password=get_config().BURRITO_DB_PASSWORD,
            host=get_config().BURRITO_DB_HOST,
            port=int(get_config().BURRITO_DB_PORT),
            charset="utf8mb4"
        )

    except OperationalError as exc:
        raise MySQLConnectionError(str(exc)) from exc

    except Exception as exc:
        raise DBConnectionError(str(exc)) from exc
