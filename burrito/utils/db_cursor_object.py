from peewee import MySQLDatabase

from burrito.utils.singleton_pattern import singleton


@singleton
class BurritoDatabaseCursor(MySQLDatabase):
    def __init__(self, database, **kwargs) -> None:
        super().__init__(database, **kwargs)


def get_database_cursor() -> BurritoDatabaseCursor:
    """_summary_

    Create data base cursor

    Returns:
        BurritoDatabaseCursor: current database cursor
    """

    return BurritoDatabaseCursor(
        "burrito",
        user="burrito_user", password="Qwerty123",
        host="192.168.0.173", port=3306
    )
