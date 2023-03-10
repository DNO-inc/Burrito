from burrito.models.issues_model import pg_issues_db, Issues
from burrito.models.roles_model import pg_roles_db, Roles
from burrito.models.statuses_model import pg_statuses_db, Statuses
from burrito.models.tags_model import pg_tags_db, Tags
from burrito.models.user_model import pg_users_db, Users


def create_tables():
    pg_tags_db.create_tables((Tags,))
    pg_statuses_db.create_tables((Statuses,))

    pg_issues_db.create_tables((Issues,))
    pg_roles_db.create_tables((Roles,))
    pg_users_db.create_tables((Users,))
