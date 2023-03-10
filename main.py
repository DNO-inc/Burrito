
from fastapi import FastAPI

from apps.about.router import about_router
from apps.registration.router import registration_router

from utils.db_utils import create_tables
from utils.app_util import connect_app



create_tables()


app = FastAPI()
connect_app(app, "/about", about_router)
connect_app(app, "/registration", registration_router)

# D.N.O


