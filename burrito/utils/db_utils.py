
from burrito.models.issues_model import pg_issues_db, Issues
from burrito.models.user_model import pg_users_db, Users


def create_tables():
    pg_issues_db.create_tables((Issues,))
    pg_users_db.create_tables((Users,))
