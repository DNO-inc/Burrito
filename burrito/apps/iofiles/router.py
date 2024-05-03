from fastapi import APIRouter

from .views import (
    iofiles__upload_file_for_ticket,
    iofiles__get_file,
    iofiles__get_file_ids,
    iofiles__delete_file
)


iofiles_router = APIRouter()

iofiles_router.add_api_route(
    "/",
    iofiles__upload_file_for_ticket,
    methods=["POST"]
)

iofiles_router.add_api_route(
    "/file_ids/{ticket_id}",
    iofiles__get_file_ids,
    methods=["GET"]
)

iofiles_router.add_api_route(
    "/{file_id}",
    iofiles__delete_file,
    methods=["DELETE"]
)

iofiles_router.add_api_route(
    "/{file_id}",
    iofiles__get_file,
    methods=["GET"]
)
