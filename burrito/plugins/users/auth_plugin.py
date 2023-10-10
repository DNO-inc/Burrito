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
            get_logger().info(
                f"""
                    Failed to access user info:
                        * status: {response["status"]}
                        * result: {response["result"]}

                """
            )

            raise ValueError

        return {
            "user_id": response["result"]["info1"][0]["ID_NUM"],
            "firstname": response["result"]["name"],
            "lastname": response["result"]["surname"],
            "faculty": response["result"]["info1"][0]["KOD_DIV"],
            "group": response["result"]["info1"][0]["KOD_GROUP"],
            "email": response["result"]["email"]
        }
