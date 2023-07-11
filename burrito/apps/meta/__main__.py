from multiprocessing import Process

import uvicorn

from fastapi.openapi.utils import get_openapi_path
from burrito.utils.config_reader import get_config
from burrito.containers import prepare_app
from burrito.utils.app_util import get_current_app


if prepare_app():
    from burrito.apps.meta.router import meta_router


app = get_current_app()
app.add_api_route("/meta", meta_router)


@app.get("/docs", include_in_schema=False)
async def docs(r):
    return get_openapi_path()


def test():
    uvicorn.run(
        "burrito.apps.meta.__main__:app",
        host="0.0.0.0",
        port=int(get_config().BURRITO_PORT_META),
        proxy_headers=bool(get_config().BURRITO_PROXY_HEADERS)
    )


p = Process(target=test)
p.start()
p.join()

