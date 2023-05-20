"""_summary_

Main Burrito file, that run REST API service and run all tasks,
needed for Burrito functionality.

"""

import uvicorn

from burrito.apps.registration.router import registration_router
from burrito.apps.about.router import about_router

from burrito.apps.auth.router import auth_router
from burrito.apps.profile.router import profile_router

from burrito.apps.tickets.router import tickets_router
from burrito.apps.admin.router import admin_router

from burrito.apps.anon.router import anon_router
from burrito.apps.meta.router import meta_router

from burrito.utils.db_utils import create_tables
from burrito.utils.app_util import connect_app, get_current_app
#from burrito.utils.db_preprocessor import LocalDataBasePreprocessor


create_tables()

#db_preprocessor = LocalDataBasePreprocessor(
#    {"filename": "/mnt/d/pyrus/Ramee/preprocessor_config.json"}
#)
#db_preprocessor.apply_data()


app = get_current_app()
connect_app(app, "/about", about_router)
connect_app(app, "/registration", registration_router)
connect_app(app, "/profile", profile_router)
connect_app(app, "/auth", auth_router)
connect_app(app, "/tickets", tickets_router)
connect_app(app, "/admin", admin_router)
connect_app(app, "/anon", anon_router)
connect_app(app, "/meta", meta_router)


if __name__ == "__main__":
    uvicorn.run(
        "burrito.__main__:app",
        host="0.0.0.0",
        port=8080,
        server_header=False,
        reload=True,
        reload_dirs="burrito"
    )
