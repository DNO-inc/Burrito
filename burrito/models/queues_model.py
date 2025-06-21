from peewee import AutoField, CharField, ForeignKeyField

from burrito.models.basic_model import BurritoBasicModel
from burrito.models.division_model import Divisions


class Queues(BurritoBasicModel):
    queue_id = AutoField()

    name = CharField(max_length=255)
    division = ForeignKeyField(
        Divisions,
        field="division_id",
        on_delete="NO ACTION"
    )
    scope = CharField(max_length=50)

    class Meta:
        depends_on = [Divisions]
