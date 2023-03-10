import uvicorn
from fastapi import FastAPI

from burrito.apps.registration.router import registration_router
from burrito.apps.about.router import about_router

from burrito.utils.db_utils import create_tables
from burrito.utils.app_util import connect_app

create_tables()

app = FastAPI()
connect_app(app, "/about", about_router)
connect_app(app, "/registration", registration_router)

if __name__ == "__main__":
    uvicorn.run("burrito.__main__:app", port=8080, reload=True)
