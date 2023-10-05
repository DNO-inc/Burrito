import requests
import pymysql.cursors
import orjson as json

from burrito.utils.task_manager import get_task_manager
from burrito.utils.config_reader import get_config
from burrito.utils.logger import get_logger
from burrito.utils.db_cursor_object import get_database_cursor

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

DEFAULT_CONFIG = ""

with open("preprocessor_config.json", "r", encoding="utf-8") as file:
    DEFAULT_CONFIG = json.loads(file.read())


SSU_GROUPS_URL = "https://iis.sumdu.edu.ua/api/getGroups"
SSU_FACULTIES_URL = "https://iis.sumdu.edu.ua/api/getDivisions"


def pull_faculties_from_ssu() -> list:
    try:
        raw_faculties_data = requests.get(
            f"{SSU_FACULTIES_URL}?key={get_config().BURRITO_SSU_KEY}",
            timeout=30
        )
        if raw_faculties_data.status_code != 200:
            get_logger().warning(
                f"{SSU_FACULTIES_URL}  status code is {raw_faculties_data.status_code}"
            )
        raw_faculties_data = raw_faculties_data.json()["result"]

        return [
            {
                "faculty_id": raw_group["ID_DIV"],
                "name": raw_group["ABBR_DIV"]
            } for raw_group in raw_faculties_data if (
                raw_group["ID_DIV"] and raw_group["ABBR_DIV"] and raw_group["KOD_TYPE"] in (7, 9)
            )
        ]
    except Exception as e:
        get_logger().error(e)

    return []


def pull_groups_from_ssu() -> list:
    try:
        raw_groups_data = requests.get(
            f"{SSU_GROUPS_URL}?key={get_config().BURRITO_SSU_KEY}",
            timeout=30
        )
        if raw_groups_data.status_code != 200:
            get_logger().warning(
                f"{SSU_GROUPS_URL}  status code is {raw_groups_data.status_code}"
            )
        raw_groups_data = raw_groups_data.json()["result"]

        return [
            {
                "group_id": raw_group["ID_GROUP"],
                "name": raw_group["NAME_GROUP"]
            } for raw_group in raw_groups_data if raw_group["ID_GROUP"] and raw_group["NAME_GROUP"]
        ]
    except Exception as e:
        get_logger().error(e)

    return []


def preprocessor_task():
    get_logger().info("Preprocessor is started")

    conn = None

    try:
        conn = pymysql.connect(
            database=get_config().BURRITO_DB_NAME,
            user=get_config().BURRITO_DB_USER,
            password=get_config().BURRITO_DB_PASSWORD,
            host=get_config().BURRITO_DB_HOST,
            port=int(get_config().BURRITO_DB_PORT),
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        get_logger().warning(e)
        return

    with conn:
        __sql_commands: dict = {}
        __config_data: dict = {}

        data: dict = DEFAULT_CONFIG
        data["groups"] = pull_groups_from_ssu()
        data["faculties"] += pull_faculties_from_ssu()

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
                        if table in ("groups", "faculties"):
                            get_task_manager().add_task(MODEL_KEYS[table].create, **value)
                        else:
                            if table == "queues":
                                get_database_cursor().execute_sql("SET FOREIGN_KEY_CHECKS=0")
                            MODEL_KEYS[table].create(**value)
                            if table == "queues":
                                get_database_cursor().execute_sql("SET FOREIGN_KEY_CHECKS=1")
                    except Exception as e:
                        get_logger().warning(f"Preprocessor error: {e}")

    get_logger().info("Preprocessor sub-tasks pushed to task manager")
