from peewee import AutoField, CharField, IntegerField

from burrito.models.basic_model import BurritoBasicModel


class Roles(BurritoBasicModel):
    role_id = AutoField()
    name = CharField(32)
    priority = IntegerField(null=False)
