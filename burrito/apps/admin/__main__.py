import uvicorn
from random import randint
from fastapi.routing import APIRoute

from burrito.utils.config_reader import get_config
from burrito.containers import prepare_app
from burrito.utils.app_util import get_current_app, connect_app


if prepare_app():
    from burrito.apps.admin.router import admin_router
else:
    print("App preparation failed")


app = get_current_app(docs_url="/admin/docs", openapi_url="/admin/openapi.json")
connect_app(app, "/admin", admin_router)


if __name__ == "__main__":
    uvicorn.run(
        "burrito.apps.admin.__main__:app",
        host="0.0.0.0",
        port=int(get_config().BURRITO_PORT_ADMIN),
        proxy_headers=bool(get_config().BURRITO_PROXY_HEADERS)
    )
