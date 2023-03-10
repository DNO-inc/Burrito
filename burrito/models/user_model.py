from peewee import PostgresqlDatabase
from peewee import Model, CharField, TextField, PrimaryKeyField, DateTimeField

pg_users_db = PostgresqlDatabase(
    "postgres",
    user="postgres", password="root",
    host="localhost", port=5432
)


class Users(Model):
    user_id = PrimaryKeyField()
    firstname = CharField(60)
    lastname = CharField(60)

    login = CharField(25)
    hashed_password = TextField()

    phone = CharField(15)
    email = CharField(255)

    registration_date = DateTimeField()

    class Meta:
        database = pg_users_db
