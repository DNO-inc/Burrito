import requests

from burrito.plugins.base_plugin import BurritoBasePlugin
from burrito.utils.config_reader import get_config
from burrito.utils.logger import get_logger

SSU_FACULTIES_URL = "https://iis.sumdu.edu.ua/api/getDivisions"

__PLUGIN_CLASS = "FacultyPlugin"


class FacultyPlugin(BurritoBasePlugin):
    plugin_name: str = "faculty_updates"

    @staticmethod
    def execute(*args, **kwargs):
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
