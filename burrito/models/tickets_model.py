from peewee import (
    AutoField,
    IntegerField, TextField,
    DateTimeField, BooleanField,
    CharField, ForeignKeyField
)

from burrito.utils.date import get_datetime_now

from burrito.models.queues_model import Queues
from burrito.models.statuses_model import Statuses
from burrito.models.faculty_model import Faculties
from burrito.models.user_model import Users
from burrito.models.basic_model import BurritoBasicModel


class Tickets(BurritoBasicModel):
    ticket_id = AutoField()

    creator = ForeignKeyField(
        Users,
        field="user_id",
        on_delete="NO ACTION"
    )

    assignee = ForeignKeyField(
        Users,
        field="user_id",
        on_delete="NO ACTION",
        null=True
    )

    subject = CharField(255)
    body = TextField()

    hidden = BooleanField(default=False)
    anonymous = BooleanField(default=False)

    upvotes = IntegerField(default=0)

    created = DateTimeField(default=get_datetime_now)

    faculty = ForeignKeyField(
        Faculties,
        field="faculty_id",
        on_delete="NO ACTION"
    )

    queue = ForeignKeyField(
        Queues,
        field="queue_id",
        on_delete="NO ACTION",
        null=True
    )

    status = ForeignKeyField(
        Statuses,
        field="status_id",
        on_delete="NO ACTION",
        default=1
    )

    class Meta:
        depends_on = [Users, Queues, Faculties, Statuses]
