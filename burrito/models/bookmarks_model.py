from peewee import ForeignKeyField

from burrito.models.user_model import Users
from burrito.models.tickets_model import Tickets
from burrito.models.basic_model import BurritoBasicModel


class Bookmarks(BurritoBasicModel):
    user_id = ForeignKeyField(
        Users,
        field="user_id",
        on_delete="NO ACTION"
    )

    ticket_id = ForeignKeyField(
        Tickets,
        field="ticket_id",
        on_delete="NO ACTION"
    )

    class Meta:
        depends_on = [Users, Tickets]
