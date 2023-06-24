from peewee import AutoField, CharField

from burrito.models.basic_model import BurritoBasicModel


class Permissions(BurritoBasicModel):
    permission_id = AutoField()
    name = CharField(max_length=20)
