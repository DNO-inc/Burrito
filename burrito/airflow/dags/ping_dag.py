import socket
import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.baseoperator import chain

from burrito.utils.logger import get_logger
from burrito.utils.config_reader import get_config


HOSTS_TO_PING = (
    (get_config().BURRITO_DB_HOST, get_config().BURRITO_DB_PORT),
    (get_config().BURRITO_REDIS_HOST, get_config().BURRITO_REDIS_PORT),
    (get_config().BURRITO_MONGO_HOST, get_config().BURRITO_MONGO_PORT),
    ("iis.sumdu.edu.ua", 80),
    (get_config().BURRITO_SMTP_SERVER, 25),
    (get_config().BURRITO_SMTP_SERVER, 465),
)


def burrito_ping(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host, int(port)))
    except socket.error:
        get_logger().critical(f"({host}, {port}) is unreachable")
    except Exception as exc:
        get_logger().error(exc)


with DAG(
    dag_id="ping_dag",
    description="Pinging important hosts",
    start_date=datetime.datetime.now() - datetime.timedelta(days=1),
    schedule_interval=datetime.timedelta(hours=1),
    catchup=False,
    is_paused_upon_creation=False
) as dag:
    chain(
        *[
            PythonOperator(
                task_id=f"pinging__{host}_{port}",
                python_callable=burrito_ping,
                op_kwargs={
                    "host": host,
                    "port": port
                }
            ) for host, port in HOSTS_TO_PING
        ]
    )
