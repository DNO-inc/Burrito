import json
from pathlib import Path
import os

import pymysql.cursors

from burrito.init.init_task import InitTask
from burrito.utils.config_reader import get_config

from burrito.models.group_model import Groups
from burrito.models.statuses_model import Statuses
from burrito.models.faculty_model import Faculties
from burrito.models.queues_model import Queues
from burrito.models.permissions_model import Permissions
from burrito.models.roles_model import Roles
from burrito.models.role_permissions_model import RolePermissions


MODEL_KEYS = {
    "groups": Groups,
    "faculties": Faculties,
    "statuses": Statuses,
    "queues": Queues,
    "permissions": Permissions,
    "roles": Roles,
    "role_permissions": RolePermissions
}


class PreProcessorTask(InitTask):
    def __init__(self, wait_time: int = 30, attempt_count: int = 2, can_skip: bool = False) -> None:
        super().__init__(wait_time, attempt_count, can_skip)

    def run(self):
        __config_path = Path(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
        ) / "preprocessor_config.json"

        if not os.path.exists(__config_path):
            raise FileNotFoundError("preprocessor_config.json is not found")

        conn = pymysql.connect(
            database=get_config().BURRITO_DB_NAME,
            user=get_config().BURRITO_DB_USER,
            password=get_config().BURRITO_DB_PASSWORD,
            host=get_config().BURRITO_DB_HOST,
            port=int(get_config().BURRITO_DB_PORT),
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn:
            __sql_commands: dict = {}
            __config_data: dict = {}
            data: dict = None

            with open(__config_path, "r", encoding="utf-8") as file:
                data = json.loads(file.read())

            for key, value in data.items():
                if not key.startswith("__"):
                    __config_data[key] = value
                    continue

                if key == "__tables_option":
                    __sql_commands = value

            for table, config_values in __config_data.items():
                with conn.cursor() as cursor:
                    cursor.execute(__sql_commands[table])
                conn.commit()

                config_filtered_values: set = {tuple(i.values()) for i in config_values}
                db_filtered_values: set = {tuple(i.values()) for i in cursor.fetchall()}

                if config_filtered_values.difference(db_filtered_values):
                    for value in config_values:
                        try:
                            MODEL_KEYS[table].create(**value)
                        except:
                            ...
