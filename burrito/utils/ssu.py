import requests

from burrito.utils.logger import get_logger


class CabinetUser:

    def __init__(self, key: str, token: str):

        params = {
            "key": key,
            "token": token
        }

        response = requests.get("https://cabinet.sumdu.edu.ua/api/getPersonInfo", params=params).json()

        if response["status"] != "OK":
            get_logger().info(
                f"""
                    Failed to access user info:
                        * status: {response["status"]}
                        * result: {response["result"]}

                """
            )

            raise ValueError

        self.user_id = response["result"]["info1"][0]["ID_NUM"]
        self.firstname = response["result"]["name"]
        self.lastname = response["result"]["surname"]
        self.faculty = response["result"]["info1"][0]["KOD_DIV"]
        self.group = response["result"]["info1"][0]["KOD_GROUP"]
        self.email = response["result"]["email"]

