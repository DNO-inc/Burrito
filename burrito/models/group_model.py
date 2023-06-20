from peewee import AutoField, CharField

from burrito.models.basic_model import BurritoBasicModel


class Groups(BurritoBasicModel):
    group_id = AutoField()
    name = CharField(10)
