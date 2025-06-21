import requests

from burrito.plugins.base_plugin import BurritoBasePlugin
from burrito.utils.logger import get_logger

__PLUGIN_CLASS = "AuthSSUPlugin"


class AuthSSUPlugin(BurritoBasePlugin):
    plugin_name: str = "third_party_auth"

    @staticmethod
    def execute(*args, **kwargs):
        params = {
            "key": kwargs["key"],
            "token": kwargs["token"]
        }

        response = requests.get(
            "https://cabinet.sumdu.edu.ua/api/getPersonInfo",
            params=params,
            timeout=10
        ).json()

        if response["status"] != "OK":
            get_logger().error(
                f"""
                    Failed to access user info:
                        * status: {response["status"]}
                        * result: {response["result"]}

                """
            )

            raise ValueError

        is_student = True
        if response["result"].get("info2"):
            is_student = False

        get_logger().info(response)

        response_result: dict = response["result"]

        return {
            "user_id": response_result["guid"],
            "firstname": response_result["name"],
            "lastname": response_result["surname"],
            "division_id": response_result["info1"][-1]["KOD_DIV"] if is_student else 1,
            "group_id": response_result["info1"][-1]["KOD_GROUP"] if is_student else None,
            "email": response_result["email"],
        }
