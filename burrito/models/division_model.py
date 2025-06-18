from peewee import AutoField, CharField

from burrito.models.basic_model import BurritoBasicModel


class Divisions(BurritoBasicModel):
    division_id = AutoField()
    name = CharField(32)
