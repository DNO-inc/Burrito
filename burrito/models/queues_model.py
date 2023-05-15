from peewee import Model, AutoField, ForeignKeyField, CharField

from burrito.models.faculty_model import Faculties

from burrito.utils.db_cursor_object import get_database_cursor


class Queues(Model):
    queue_id = AutoField()

    name = CharField(max_length=255)
    faculty = ForeignKeyField(
        Faculties,
        field="faculty_id",
        on_delete="NO ACTION"
    )

    class Meta:
        database = get_database_cursor()
        depends_on = [Faculties]
