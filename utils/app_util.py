
from fastapi import FastAPI, APIRouter



def connect_app(fast_api_object: FastAPI, prefix: str, router: APIRouter):
    fast_api_object.include_router(router=router, prefix=prefix)

