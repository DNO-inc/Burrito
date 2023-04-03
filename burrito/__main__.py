"""_summary_

Main Burrito file, that run REST API service and run all tasks,
needed for Burrito functionality.

"""

import uvicorn

from burrito.apps.registration.router import registration_router
from burrito.apps.about.router import about_router

from burrito.apps.auth.router import auth_router
from burrito.apps.profile.router import profile_router

from burrito.apps.reports.router import reports_router

from burrito.utils.db_utils import create_tables
from burrito.utils.app_util import connect_app, get_current_app


create_tables()

app = get_current_app()
connect_app(app, "/about", about_router)
connect_app(app, "/registration", registration_router)
connect_app(app, "/profile", profile_router)
connect_app(app, "/auth", auth_router)
connect_app(app, "/reports", reports_router)


if __name__ == "__main__":
    uvicorn.run("burrito.__main__:app", port=8080, reload=True)
