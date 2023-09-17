from bson.objectid import ObjectId

from fastapi import HTTPException
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ServerSelectionTimeoutError

from burrito.utils.singleton_pattern import singleton
from burrito.utils.config_reader import get_config
from burrito.utils.logger import get_logger

from burrito.models.m_basic_model import MongoBaseModel


__AUTH_STRING = f'mongodb://{get_config().BURRITO_MONGO_USER}:{get_config().BURRITO_MONGO_PASSWORD}@{get_config().BURRITO_MONGO_HOST}:{get_config().BURRITO_MONGO_PORT}'


@singleton
class MongoConnector(MongoClient):
    def __init__(self, host: str, port: int = 27017, **kwargs) -> None:
        super().__init__(host, port, **kwargs)


def get_mongo_cursor():
    mongo_cursor = MongoConnector(__AUTH_STRING)

    try:
        mongo_cursor.admin.command("ping")
    except ServerSelectionTimeoutError as exc:
        get_logger().critical("Mongo server is unavailable")
        raise HTTPException(
            status_code=500,
            detail="Some of the services is unavailable, please try late"
        ) from exc

    return mongo_cursor


_MONGO_CURSOR = get_mongo_cursor()
_MONGO_DB_NAME = get_config().BURRITO_MONGO_DB


def mongo_insert(model: MongoBaseModel):
    return str(_MONGO_CURSOR[_MONGO_DB_NAME][model.Meta.table_name].insert_one(model.dict()).inserted_id)


def mongo_select(
        model: MongoBaseModel,
        start_page: int = 1,
        items_count: int = 10,
        sort_by: str = "",
        desc: bool = False,
        **filters
) -> list[object]:
    if sort_by:
        return list(
            _MONGO_CURSOR[_MONGO_DB_NAME][model.Meta.table_name].find(filters).skip(
                (start_page - 1) * items_count
            ).limit(items_count).sort(
                sort_by,
                DESCENDING if desc else ASCENDING
            )
        )

    return list(
        _MONGO_CURSOR[_MONGO_DB_NAME][model.Meta.table_name].find(filters).skip(
            (start_page - 1) * items_count
        ).limit(items_count)
    )


def mongo_update(model: MongoBaseModel, **filters) -> list[object]:
    item_id = filters.get("_id")
    if item_id and isinstance(item_id, str):
        filters["_id"] = ObjectId(item_id)

    _MONGO_CURSOR[_MONGO_DB_NAME][model.Meta.table_name].update_many(
        filters, {"$set": model.dict()}
    )


def mongo_delete(model: MongoBaseModel, **filters) -> None:
    _MONGO_CURSOR[_MONGO_DB_NAME][model.Meta.table_name].delete_many(filters)
