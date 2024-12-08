"""_summary_

Main Burrito file, that run REST API service and run all tasks,
needed for Burrito functionality.

"""

from burrito.plugins.loader import PluginLoader
from burrito.utils.db_utils import create_tables
from burrito.utils.tasks.preprocessor import preprocessor_task

PluginLoader.load()
create_tables()
preprocessor_task()


if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI
    from uvicorn.config import LOGGING_CONFIG

    from burrito.apps.about.router import about_router
    from burrito.apps.admin.router import admin_router
    from burrito.apps.anon.router import anon_router
    from burrito.apps.auth.router import auth_router
    from burrito.apps.comments.router import comments_router
    from burrito.apps.iofiles.router import iofiles_router
    from burrito.apps.meta.router import meta_router
    from burrito.apps.notifications.router import notifications_router
    from burrito.apps.notifications.utils import email_loop
    from burrito.apps.profile.router import profile_router
    from burrito.apps.registration.router import registration_router
    from burrito.apps.scheduler.core import start_scheduler
    from burrito.apps.statistic.router import statistic_router
    from burrito.apps.tickets.router import tickets_router
    from burrito.apps.ws.utils import run_websocket_server
    from burrito.models.m_email_code import EmailVerificationCode
    from burrito.models.m_password_rest_model import AccessRenewMetaData
    from burrito.utils.app_util import connect_app, get_current_app
    from burrito.utils.config_reader import get_config
    from burrito.utils.mongo_util import mongo_init_ttl_indexes
    from burrito.utils.task_manager import get_task_manager

    mongo_init_ttl_indexes([EmailVerificationCode, AccessRenewMetaData])

    app: FastAPI = get_current_app()
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
    connect_app(app, "/notifications", notifications_router)
    connect_app(app, "/statistic", statistic_router)

    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "[ %(asctime)s ] | %(name)s (%(process)d) | %(levelprefix)s %(message)s"
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = "[ %(asctime)s ] | %(name)s (%(process)d) | %(levelprefix)s %(client_addr)s - \"%(request_line)s\" %(status_code)s"

    config = uvicorn.Config(
        app,  # "burrito.__main__:app",
        host="0.0.0.0",
        port=int(get_config().BURRITO_PORT),
        proxy_headers=bool(get_config().BURRITO_PROXY_HEADERS),
    )
    uvicorn_server = uvicorn.Server(config)

    task_manager = get_task_manager()

    task_manager.add_task(run_websocket_server, daemon=True)
    task_manager.add_task(start_scheduler, daemon=True)
    task_manager.add_task(email_loop, daemon=True)
    task_manager.add_task(uvicorn_server.serve())
    task_manager.run(forever=False)
