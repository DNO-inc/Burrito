from fastapi import FastAPI, APIRouter

# from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

# from burrito.middlewares.user_agent import UserAgentMiddleware

from burrito.preprocessor.core import preprocessor_task

from .singleton_pattern import singleton
from .task_manager import get_async_manager
from .logger import get_logger


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

    app = BurritoApi(docs_url=docs_url, openapi_url=openapi_url)

    app.add_event_handler("startup", startup_event)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


async def startup_event():
    """_summary_

    Setup task when when server is started
    """

    task_manager = get_async_manager()
    task_manager.add_task(preprocessor_task())

#    task_manager.add_task(get_pubsub_manager().run())

    def test1():
        print("test1")

    async def test2():
        print("test2")

#    get_pubsub_manager().add_callback("test1", test1)
#    get_pubsub_manager().add_callback("test2", test2)

    task_manager.run()

    get_logger().info("All tasks was started")


def connect_app(fast_api_object: FastAPI, prefix: str, router: APIRouter):
    """_summary_

        Args:
        fast_api_object (FastAPI): main FastApi router
        prefix (str): app url
        router (APIRouter): application router
    """

    fast_api_object.include_router(router=router, prefix=prefix)
