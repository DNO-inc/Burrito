import uvicorn

from burrito.apps.notifications.router import notifications_router
from burrito.apps.notifications.utils import email_loop
from burrito.containers import get_current_app_name
from burrito.utils.app_util import connect_app, get_current_app
from burrito.utils.config_reader import get_config
from burrito.utils.task_manager import get_task_manager

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
