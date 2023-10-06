import uvicorn

from burrito.containers import get_current_app_name
from burrito.apps.notifications.router import notifications_router
from burrito.utils.config_reader import get_config
from burrito.utils.app_util import get_current_app, connect_app
from burrito.utils.task_manager import get_task_manager

from burrito.apps.notifications.utils import email_loop


_APP_NAME = get_current_app_name()

app = get_current_app(docs_url=f"/{_APP_NAME}/", openapi_url=f"/{_APP_NAME}/openapi.json")
connect_app(app, f"/{_APP_NAME}", notifications_router)


if __name__ == "__main__":
    config = uvicorn.Config(
        f"burrito.apps.{_APP_NAME}.__main__:app",
        host="0.0.0.0",
        port=int(get_config().BURRITO_PORT),
        proxy_headers=bool(get_config().BURRITO_PROXY_HEADERS),
    )
    uvicorn_server = uvicorn.Server(config)

    task_manager = get_task_manager()

    task_manager.add_task(email_loop, daemon=True)
    task_manager.add_task(uvicorn_server.serve())
    task_manager.run(forever=False)
