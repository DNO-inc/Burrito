import datetime

from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.python import PythonOperator
from peewee import MySQLDatabase

from burrito.airflow.utils import preprocessor_task
from burrito.models.m_email_code import EmailVerificationCode
from burrito.models.m_password_rest_model import AccessRenewMetaData
from burrito.utils.db_cursor_object import get_database_cursor
from burrito.utils.db_utils import create_tables
from burrito.utils.logger import get_logger
from burrito.utils.mongo_util import mongo_init_ttl_indexes


def init_db_events():
    with open(
        "/opt/burrito_project/burrito/event_init.sql",
        "r",
        encoding="utf-8"
    ) as file:
        db: MySQLDatabase = get_database_cursor()

        for query in file.read().split(";"):
            query = query.replace('\t', "").replace("\n", "")
            query = ' '.join(query.split())

            if not query:
                continue

            try:
                db.execute_sql(query)
            except Exception as e:
                get_logger().error(e)


with DAG(
    dag_id="preinstall_dag",
    description="Preparing DB",
    start_date=datetime.datetime.now() - datetime.timedelta(days=1),
    schedule_interval=None,
    is_paused_upon_creation=False
) as dag:
    chain(
        PythonOperator(
            task_id="create_db_tables",
            python_callable=create_tables
        ),
        PythonOperator(
            task_id="first_preprocessor_run",
            python_callable=preprocessor_task
        ),
        PythonOperator(
            task_id="create_mongo_ttl_indexes",
            python_callable=mongo_init_ttl_indexes,
            op_kwargs={
                "models": [EmailVerificationCode, AccessRenewMetaData]
            }
        ),
        PythonOperator(
            task_id="create_db_events",
            python_callable=init_db_events
        )
    )
