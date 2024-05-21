import os
import time

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pymongo.errors import ServerSelectionTimeoutError
import peewee

from burrito.utils.exceptions import (
    DBConnectionError,
    db_connection_error_handler
)
from burrito.utils.singleton_pattern import singleton
from burrito.utils.task_manager import get_task_manager
from burrito import CURRENT_TIME_ZONE


@singleton
class BurritoApi(FastAPI):
    """_summary_

    Main application object
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


def get_current_app(*, docs_url="/docs", openapi_url="/openapi.json") -> BurritoApi:
    """_summary_

    Return current application object

    Returns:
        BurritoApi: current application object
    """

    app: FastAPI = BurritoApi(docs_url=docs_url, openapi_url=openapi_url)

    app.add_exception_handler(
        DBConnectionError,
        db_connection_error_handler
    )
    app.add_exception_handler(
        ServerSelectionTimeoutError,
        db_connection_error_handler
    )
    app.add_exception_handler(
        peewee.OperationalError,
        db_connection_error_handler
    )
    app.add_event_handler("startup", startup_event)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    os.environ['TZ'] = str(CURRENT_TIME_ZONE)
    time.tzset()

    return app


async def startup_event():
    """_summary_

    Setup task when when server is started
    """

    get_task_manager().run()


def connect_app(fast_api_object: FastAPI, prefix: str, router: APIRouter):
    """_summary_

        Args:
        fast_api_object (FastAPI): main FastApi router
        prefix (str): app url
        router (APIRouter): application router
    """

    fast_api_object.include_router(router=router, prefix=prefix)
