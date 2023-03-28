from peewee import PostgresqlDatabase

from burrito.utils.singleton_pattern import singleton


@singleton
class PostgresqlCursor(PostgresqlDatabase):
    def __init__(self, database, **kwargs) -> None:
        super().__init__(database, **kwargs)


def get_database_cursor() -> PostgresqlDatabase:
    """Create data base cursor"""

    return PostgresqlDatabase(
        "ramee",
        user="postgres", password="root",
        host="localhost", port=5432
    )
