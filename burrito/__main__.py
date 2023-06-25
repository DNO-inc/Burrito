"""_summary_

Main Burrito file, that run REST API service and run all tasks,
needed for Burrito functionality.

"""

from burrito.utils.config_reader import get_config

from burrito.init.init_system import InitManager, get_logger
from burrito.init.tasks.check_db_task import CheckDBTask

get_config()  # read configs

init_manager = InitManager(
    error_attempt_delta=3
)
init_manager.add_task(CheckDBTask(attempt_count=100))

init_manager.run_cycle()

#from burrito.utils.db_preprocessor import LocalDataBasePreprocessor
#db_preprocessor = LocalDataBasePreprocessor(
#    {"filename": "./preprocessor_config.json"}
#)
#db_preprocessor.apply_data()


if not init_manager.critical:
    import uvicorn
    from prometheus_fastapi_instrumentator import Instrumentator, metrics

    from burrito.apps.registration.router import registration_router
    from burrito.apps.about.router import about_router

    from burrito.apps.auth.router import auth_router
    from burrito.apps.profile.router import profile_router

    from burrito.apps.tickets.router import tickets_router
    from burrito.apps.admin.router import admin_router

    from burrito.apps.anon.router import anon_router
    from burrito.apps.meta.router import meta_router

    from burrito.apps.iofiles.router import iofiles_router
    from burrito.apps.comments.router import comments_router

    from burrito.utils.app_util import connect_app, get_current_app
else:
    print()
    get_logger().critical("Some critical error was ocurred before")
    exit(1)


app = get_current_app()
connect_app(app, "/about", about_router)
connect_app(app, "/registration", registration_router)
connect_app(app, "/profile", profile_router)
connect_app(app, "/auth", auth_router)
connect_app(app, "/tickets", tickets_router)
connect_app(app, "/admin", admin_router)
connect_app(app, "/anon", anon_router)
connect_app(app, "/meta", meta_router)
connect_app(app, "/iofiles", iofiles_router)
connect_app(app, "/comments", comments_router)

# connect prometheus
instrumentator = Instrumentator().instrument(app)
instrumentator.add(
    metrics.request_size(
        should_include_handler=True,
        should_include_method=False,
        should_include_status=True,
        metric_namespace="a",
        metric_subsystem="b",
    )
).add(
    metrics.response_size(
        should_include_handler=True,
        should_include_method=False,
        should_include_status=True,
        metric_namespace="namespace",
        metric_subsystem="subsystem",
    )
)

instrumentator.expose(app)

if __name__ == "__main__":

    uvicorn.run(
        "burrito.__main__:app",
        host="0.0.0.0",
        port=int(get_config().BURRITO_PORT),
        proxy_headers=bool(get_config().BURRITO_PROXY_HEADERS),
        reload=True,
        reload_dirs="burrito"
    )
