import uvicorn

from burrito.utils.config_reader import get_config
from burrito.containers import prepare_app, get_current_app_name
from burrito.utils.app_util import get_current_app, connect_app


if prepare_app():
    from burrito.apps.notifications.router import notifications_router
else:
    print("App preparation failed")

_APP_NAME = get_current_app_name()

app = get_current_app(docs_url=f"/{_APP_NAME}/", openapi_url=f"/{_APP_NAME}/openapi.json")
connect_app(app, f"/{_APP_NAME}", notifications_router)


if __name__ == "__main__":
    uvicorn.run(
        f"burrito.apps.{_APP_NAME}.__main__:app",
        host="0.0.0.0",
        port=int(get_config().BURRITO_PORT),
        proxy_headers=bool(get_config().BURRITO_PROXY_HEADERS)
    )
