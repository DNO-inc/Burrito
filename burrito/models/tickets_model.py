from peewee import (
    AutoField,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    TextField,
)

from burrito.models.basic_model import BurritoBasicModel
from burrito.models.division_model import Divisions
from burrito.models.queues_model import Queues
from burrito.models.statuses_model import Statuses
from burrito.models.user_model import Users
from burrito.utils.date import get_datetime_now


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

    division = ForeignKeyField(
        Divisions,
        field="division_id",
        on_delete="NO ACTION"
    )

    queue = ForeignKeyField(
        Queues,
        field="queue_id",
        on_delete="NO ACTION",
        null=False
    )

    status = ForeignKeyField(
        Statuses,
        field="status_id",
        on_delete="NO ACTION",
        default=1
    )

    class Meta:
        depends_on = [Users, Queues, Divisions, Statuses]
