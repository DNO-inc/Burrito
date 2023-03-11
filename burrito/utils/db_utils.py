from peewee import DoesNotExist

from burrito.models.issues_model import pg_issues_db, Issues
from burrito.models.roles_model import pg_roles_db, Roles
from burrito.models.statuses_model import pg_statuses_db, Statuses
from burrito.models.tags_model import pg_tags_db, Tags
from burrito.models.user_model import pg_users_db, Users


def create_tables():
    pg_roles_db.create_tables((Roles,))
    pg_tags_db.create_tables((Tags,))
    pg_statuses_db.create_tables((Statuses,))

    pg_issues_db.create_tables((Issues,))
    pg_users_db.create_tables((Users,))


def create_user(login: str, hashed_password: str) -> bool:
    try:
        Users.create(login=login, hashed_password=hashed_password)
    except Exception as e:
        return False # TODO: write error to log-file

    return True


def get_user_by_login(login: str) -> Users | bool:
    try:
        return Users.get(Users.login == login)
    except:
        return False
