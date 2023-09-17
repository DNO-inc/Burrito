from peewee import Model

from burrito.utils.db_cursor_object import get_database_cursor


class BurritoBasicModel(Model):
    class Meta:
        database = get_database_cursor()
        legacy_table_names = False
        table_settings = ['ENGINE=InnoDB', 'DEFAULT CHARSET=utf8mb4']
