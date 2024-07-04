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

        return {
            "user_id": (
                int(response["result"]["info1"][-1]["ID_NUM"])
                if is_student
                else int(response["result"]["info2"][-1]["ID_NUM"])
            ),
            "firstname": response["result"]["name"],
            "lastname": response["result"]["surname"],
            "faculty": response["result"]["info1"][-1]["KOD_DIV"] if is_student else 1,
            "group": response["result"]["info1"][-1]["KOD_GROUP"] if is_student else None,
            "email": response["result"]["email"]
        }
