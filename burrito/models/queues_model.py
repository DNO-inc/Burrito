from peewee import AutoField, CharField, ForeignKeyField

from burrito.models.basic_model import BurritoBasicModel
from burrito.models.faculty_model import Faculties


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
