from pymongo import MongoClient

from burrito.utils.singleton_pattern import singleton
from burrito.utils.config_reader import get_config
from burrito.utils.logger import get_logger


@singleton
class MongoConnector(MongoClient):
    def __init__(self, host: str, port: int = 27017, **kwargs) -> None:
        super().__init__(host, port, **kwargs)


def get_mongo_cursor():
    mongo_cursor = MongoConnector(
        get_config().BURRITO_MONGO_HOST,
        int(get_config().BURRITO_MONGO_PORT)
    )

    mongo_cursor.admin.command("ping")
    print("111111111111111111111111111111111111111")
