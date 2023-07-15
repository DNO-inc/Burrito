from fastapi import APIRouter

from .views import iofiles__upload_file_for_ticket


iofiles_router = APIRouter()

#iofiles_router.add_api_route(
#    "/upload_file",
#    iofiles__upload_file_for_ticket,
#    methods=["POST"]
#)
