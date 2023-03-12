from peewee import PostgresqlDatabase
from peewee import Model, PrimaryKeyField, SmallIntegerField

from .user_model import Users
from .issues_model import Issues

pg_subscriptions_db = PostgresqlDatabase(
    "ramee",
    user="postgres", password="root",
    host="localhost", port=5432
)


class Subscriptions(Model):
    subscription_id = PrimaryKeyField()
    issue_id = SmallIntegerField()
    user_id = SmallIntegerField()

    class Meta:
        database = pg_subscriptions_db
