from peewee import AutoField, CharField

from burrito.models.basic_model import BurritoBasicModel


class Faculties(BurritoBasicModel):
    faculty_id = AutoField()
    name = CharField(32)
