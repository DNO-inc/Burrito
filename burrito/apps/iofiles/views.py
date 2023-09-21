from typing import Annotated

from fastapi import Depends, Form, UploadFile

from burrito.models.tickets_model import Tickets

from burrito.utils.auth import get_auth_core, BurritoJWT
from burrito.utils.tickets_util import is_ticket_exist
from burrito.utils.mongo_util import mongo_save_file, mongo_get_files
from burrito.utils.logger import get_logger


async def iofiles__upload_file_for_ticket(
    ticket_id: Annotated[int, Form(...)],
    file_list: list[UploadFile],
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload = await __auth_obj.require_access_token()

    ticket: Tickets | None = is_ticket_exist(ticket_id)

    for file_item in file_list:
        get_logger().info(
           f"User {token_payload.user_id} have uploaded file {mongo_save_file(ticket.ticket_id, await file_item.read())} ({file_item.size} bytes)"
        )


async def iofiles__get_files(
    ticket_id: Annotated[int, Form(...)],
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    await __auth_obj.require_access_token()

    is_ticket_exist(ticket_id)

    return {
        "files": mongo_get_files(ticket_id)
    }
