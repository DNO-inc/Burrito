import requests

from burrito.plugins.base_plugin import BurritoBasePlugin
from burrito.utils.config_reader import get_config
from burrito.utils.logger import get_logger


SSU_GROUPS_URL = "https://iis.sumdu.edu.ua/api/getGroups"

__PLUGIN_CLASS = "GroupsPlugin"


class GroupsPlugin(BurritoBasePlugin):
    plugin_name: str = "group_updates"

    @staticmethod
    def execute():
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
