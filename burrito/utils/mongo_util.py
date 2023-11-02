import math

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
        """
        Initialize the connection to the MongoDB server.

        Args:
            host: The hostname or IP address of the server.
            port: The port to connect to.
        """
        super().__init__(host, port, **kwargs)


def get_mongo_cursor():
    """
    Get a cursor to the database.
    """
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


def mongo_init_ttl_indexes(models: list[MongoBaseModel]):
    """Create indexes to use TTL ability of MongoDB"""

    for model in models:
        _MONGO_CURSOR[_MONGO_DB_NAME][model.Meta.table_name].create_index(
            "obj_creation_time",  # index name
            expireAfterSeconds=300
        )


def mongo_insert(model: MongoBaseModel):
    """
    Insert a model into mongo. This is a wrapper around the insert_one method.

    Args:
        model: The model to insert. Must have a table_name and a dict with keys corresponding to the model's fields.

    Returns:
        The id of the newly inserted record
    """
    return str(_MONGO_CURSOR[_MONGO_DB_NAME][model.Meta.table_name].insert_one(model.dict()).inserted_id)


def mongo_select(
        model: MongoBaseModel,
        start_page: int = 1,
        items_count: int = 10,
        sort_by: str = "",
        desc: bool = False,
        **filters
) -> list[object]:
    """
        Selects items from mongo based on filters. This is a wrapper around mongo's find () method

        Args:
            model: MongoBaseModel to use for query. Must be a subclass of MongoBaseModel
            start_page: int page number to start from.
            items_count: int number of items to return.
            sort_by: str sort by field. 
            desc: bool sort descending.

        Returns:
            list [ object ] - a list of objects that match the filters and are ordered by sort_by
    """

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
    """
    Update one or more documents in the database. Must have a '_id' field that is the ID of the document to update.

    Args:
        model: The model to update
    """
    item_id = filters.get("_id")
    if item_id and isinstance(item_id, str):
        filters["_id"] = ObjectId(item_id)

    _MONGO_CURSOR[_MONGO_DB_NAME][model.Meta.table_name].update_many(
        filters, {"$set": model.dict()}
    )


def mongo_delete(model: MongoBaseModel, **filters) -> None:
    """
    Delete documents matching the filters.

    Args:
        model: The model to delete from. Must inherit from MongoBaseModel.
    """
    item_id = filters.get("_id")
    if item_id and isinstance(item_id, str):
        filters["_id"] = ObjectId(item_id)

    _MONGO_CURSOR[_MONGO_DB_NAME][model.Meta.table_name].delete_many(filters)


def mongo_page_count(
        model: MongoBaseModel,
        items_count: int = 10,
        **filters
) -> int:
    """
        Get the number of pages in the collection that match the filters. This is useful for pagination.
        The default is 10 pages but you can override this with a more efficient implementation.

        Args:
            model: The model to query. Must be a MongoBaseModel
            items_count: The number of items to return.

        Returns:
            The number of pages in the collection that match the filters.
    """

    item_id = filters.get("_id")
    if item_id and isinstance(item_id, str):
        filters["_id"] = ObjectId(item_id)

    return math.ceil(_MONGO_CURSOR[_MONGO_DB_NAME][model.Meta.table_name].count_documents(filters) / items_count)


def mongo_items_count(model: MongoBaseModel, **filters) -> int:
    """
    Count of items matching the filters.

    Args:
        model: This must be a subclass of MongoBaseModel.

    Returns:
        The number of items matching the filters
    """
    item_id = filters.get("_id")
    if item_id and isinstance(item_id, str):
        filters["_id"] = ObjectId(item_id)

    return math.ceil(_MONGO_CURSOR[_MONGO_DB_NAME][model.Meta.table_name].count_documents(filters))


def mongo_save_file(ticket_id: int, file_owner_id: int, file_name: str, file: bytes, content_type: str | None) -> str:
    """
    Save a file to mongo.
    
    Args:
        ticket_id: ID of the ticket to save the file to.
        file_owner_id: Owner of the file.
        file_name: Name of the file.
        file: Bytes of the file.
        content_type
    """
    file_id = str(_MONGO_GRIDFS.put(file))

    # do something else
    if content_type is None:
        content_type = ""

    mongo_insert(
        TicketFiles(
            ticket_id=ticket_id,
            owner_id=file_owner_id,
            file_id=file_id,
            file_name=file_name,
            content_type=content_type
        )
    )

    return file_id


def mongo_get_file(file_id: str) -> bytes:
    """
    Get file from mongo.

    Args:
        file_id: id of file to get

    Returns:
        bytes of file or raise HTTPException with status code 403 if file doesn't exist in mongo or any problems appear
    """
    try:
        return _MONGO_GRIDFS.get(ObjectId(file_id)).read()
    except Exception as exc:
        raise HTTPException(
            status_code=403,
            detail=f"File with file_id {file_id} is not exists"
        ) from exc


def mongo_delete_file(file_id: str) -> None:
    """
    Delete file from mongo.

    Args:
        file_id: id of file to delete
    """
    try:
        _MONGO_GRIDFS.delete(ObjectId(file_id))
        mongo_delete(TicketFiles, file_id=ObjectId(file_id))
    except Exception as exc:
        raise HTTPException(
            status_code=403,
            detail=f"File with file_id {file_id} is not exists"
        ) from exc
