import datetime

import orjson as json
from airflow import DAG
from airflow.operators.python import PythonOperator

from burrito.airflow.utils import preprocessor_task
from burrito.models.division_model import Divisions
from burrito.models.group_model import Groups
from burrito.models.permissions_model import Permissions
from burrito.models.queues_model import Queues
from burrito.models.role_permissions_model import RolePermissions
from burrito.models.roles_model import Roles
from burrito.models.statuses_model import Statuses

MODEL_KEYS = {
    "groups": Groups,
    "divisions": Divisions,
    "statuses": Statuses,
    "queues": Queues,
    "permissions": Permissions,
    "roles": Roles,
    "role_permissions": RolePermissions
}

DEFAULT_CONFIG = ""

with open(
    "/opt/burrito_project/burrito/preprocessor_config.json",
    "r",
    encoding="utf-8"
) as file:
    DEFAULT_CONFIG = json.loads(file.read())


with DAG(
    dag_id="preprocessor_dag",
    description="Synchronize DB with data get from API",
    start_date=datetime.datetime.now() - datetime.timedelta(days=1),
    schedule_interval=datetime.timedelta(minutes=30),
    catchup=False,
    is_paused_upon_creation=False
) as dag:
    PythonOperator(
        task_id="preprocessor_task",
        python_callable=preprocessor_task
    )
