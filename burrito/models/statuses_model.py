from peewee import AutoField, CharField

from burrito.models.basic_model import BurritoBasicModel


class Statuses(BurritoBasicModel):
    status_id = AutoField()
    name = CharField(32)
