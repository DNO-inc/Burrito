import socket

from burrito.init.init_task import InitTask

from burrito.utils.config_reader import get_config
from burrito.utils.db_utils import create_tables


class CheckDBTask(InitTask):
    def __init__(self, wait_time: int = 30, attempt_count: int = 2, can_skip: bool = False) -> None:
        super().__init__(wait_time, attempt_count, can_skip)

    def run(self):
        db_host: str = get_config().BURRITO_DB_HOST
        db_port: str | int = get_config().BURRITO_DB_PORT

        if not db_host:
            raise Exception("Database host is not defined")

        if not db_port:
            raise Exception("Database port is not defined")

        if not db_port.isdigit():
            raise Exception("Database port should be integer")

        db_port = int(db_port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            sock.connect((db_host, db_port))
        except Exception as exc:
            raise Exception(f"No connection with database: {exc}")
        finally:
            sock.close()

        create_tables()
