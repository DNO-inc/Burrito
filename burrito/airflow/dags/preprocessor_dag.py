import datetime
import orjson as json

from airflow import DAG
from airflow.operators.python import PythonOperator

from burrito.models.group_model import Groups
from burrito.models.statuses_model import Statuses
from burrito.models.faculty_model import Faculties
from burrito.models.queues_model import Queues
from burrito.models.permissions_model import Permissions
from burrito.models.roles_model import Roles
from burrito.models.role_permissions_model import RolePermissions
from burrito.airflow.utils import preprocessor_task


MODEL_KEYS = {
    "groups": Groups,
    "faculties": Faculties,
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
