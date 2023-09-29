from bson.objectid import ObjectId

from fastapi import HTTPException
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ServerSelectionTimeoutError
import gridfs

from burrito.utils.singleton_pattern import singleton
from burrito.utils.config_reader import get_config
from burrito.utils.logger import get_logger

from burrito.models.m_basic_model import MongoBaseModel
from burrito.models.m_ticket_files import TicketFiles


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
_MONGO_GRIDFS: gridfs.GridFS = gridfs.GridFS(getattr(_MONGO_CURSOR, _MONGO_DB_NAME))


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
    item_id = filters.get("_id")
    if item_id and isinstance(item_id, str):
        filters["_id"] = ObjectId(item_id)

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
    item_id = filters.get("_id")
    if item_id and isinstance(item_id, str):
        filters["_id"] = ObjectId(item_id)

    _MONGO_CURSOR[_MONGO_DB_NAME][model.Meta.table_name].delete_many(filters)


def mongo_page_count(
        model: MongoBaseModel,
        items_count: int = 10,
        **filters
) -> int:
    item_id = filters.get("_id")
    if item_id and isinstance(item_id, str):
        filters["_id"] = ObjectId(item_id)

    return int(_MONGO_CURSOR[_MONGO_DB_NAME][model.Meta.table_name].count_documents(filters) / items_count)


def mongo_items_count(model: MongoBaseModel, **filters) -> int:
    item_id = filters.get("_id")
    if item_id and isinstance(item_id, str):
        filters["_id"] = ObjectId(item_id)

    return int(_MONGO_CURSOR[_MONGO_DB_NAME][model.Meta.table_name].count_documents(filters))


def mongo_save_file(ticket_id: int, file_name: str, file: bytes) -> str:
    file_id = str(_MONGO_GRIDFS.put(file))

    mongo_insert(
        TicketFiles(
            ticket_id=ticket_id,
            file_id=str(_MONGO_GRIDFS.put(file)),
            file_name=file_name
        )
    )

    return file_id


def mongo_get_file(file_id: str) -> bytes:
    try:
        return _MONGO_GRIDFS.get(ObjectId(file_id)).read()
    except Exception as exc:
        raise HTTPException(
            status_code=403,
            detail=f"File with file_id {file_id} is not exists"
        ) from exc
