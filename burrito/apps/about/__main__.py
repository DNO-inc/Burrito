import uvicorn

from burrito.apps.about.router import about_router
from burrito.containers import get_current_app_name
from burrito.utils.app_util import connect_app, get_current_app
from burrito.utils.config_reader import get_config

_APP_NAME = get_current_app_name()

app = get_current_app(docs_url=f"/{_APP_NAME}/", openapi_url=f"/{_APP_NAME}/openapi.json")
connect_app(app, f"/{_APP_NAME}", about_router)


if __name__ == "__main__":
    uvicorn.run(
        f"burrito.apps.{_APP_NAME}.__main__:app",
        host="0.0.0.0",
        port=int(get_config().BURRITO_PORT),
        proxy_headers=bool(get_config().BURRITO_PROXY_HEADERS)
    )
