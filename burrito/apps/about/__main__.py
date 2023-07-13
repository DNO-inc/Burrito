import uvicorn
from random import randint
from fastapi.routing import APIRoute

from burrito.utils.config_reader import get_config
from burrito.containers import prepare_app
from burrito.utils.app_util import get_current_app, connect_app


if prepare_app():
    from burrito.apps.about.router import about_router
else:
    print("App preparation failed")


app = get_current_app()
connect_app(app, "/about", about_router)


# TODO: temporary function, should be deleted in soon
def use_route_names_as_operation_ids(app) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name + str(randint(0, 1000))  # TODO: delete this fuc


use_route_names_as_operation_ids(app)


if __name__ == "__main__":
    uvicorn.run(
        "burrito.apps.about.__main__:app",
        host="0.0.0.0",
        port=int(get_config().BURRITO_PORT_ABOUT),
        proxy_headers=bool(get_config().BURRITO_PROXY_HEADERS)
    )
