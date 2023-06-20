from peewee import AutoField, ForeignKeyField, CharField

from burrito.models.faculty_model import Faculties

from burrito.models.basic_model import BurritoBasicModel


class Queues(BurritoBasicModel):
    queue_id = AutoField()

    name = CharField(max_length=255)
    faculty = ForeignKeyField(
        Faculties,
        field="faculty_id",
        on_delete="NO ACTION"
    )
    scope = CharField(max_length=50)

    class Meta:
        depends_on = [Faculties]
