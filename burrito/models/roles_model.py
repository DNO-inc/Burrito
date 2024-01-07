from peewee import AutoField, CharField

from burrito.models.basic_model import BurritoBasicModel


# TODO: add field 'priority'
class Roles(BurritoBasicModel):
    role_id = AutoField()
    name = CharField(32)
