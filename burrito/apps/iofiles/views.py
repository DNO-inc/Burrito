from typing import Annotated

from funcy import chunks

from fastapi import Depends, Form, UploadFile
from fastapi.responses import StreamingResponse

from burrito.models.tickets_model import Tickets
from burrito.models.m_ticket_files import TicketFiles

from burrito.utils.auth import get_auth_core, BurritoJWT
from burrito.utils.tickets_util import is_ticket_exist
from burrito.utils.mongo_util import mongo_save_file, mongo_get_file, mongo_select
from burrito.utils.logger import get_logger


async def iofiles__upload_file_for_ticket(
    ticket_id: Annotated[int, Form(...)],
    file_list: list[UploadFile],
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload = await __auth_obj.require_access_token()

    ticket: Tickets | None = is_ticket_exist(ticket_id)

    file_ids = []
    for file_item in file_list:
        current_file_id = mongo_save_file(ticket.ticket_id, file_item.filename, await file_item.read())
        get_logger().info(
           f"User {token_payload.user_id} have uploaded file {current_file_id} ({file_item.size} bytes)"
        )
        file_ids.append(current_file_id)

    return {
        "file_id": file_ids
    }


async def iofiles__get_file(
    file_id: str,
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    await __auth_obj.require_access_token()

    file_name = None
    try:
        file_name = mongo_select(TicketFiles, file_id=file_id)[0]["file_name"]
    except:
        file_name = "file"

    return StreamingResponse(
        content=(chunk for chunk in chunks(1024, mongo_get_file(file_id))),
        headers={"Content-Disposition": f"attachment; filename={file_name}"}
    )


async def iofiles__get_file_ids(
    ticket_id: Annotated[int, Form(...)],
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    await __auth_obj.require_access_token()

    is_ticket_exist(ticket_id)

    return {
        "file_ids": [TicketFiles(**item) for item in mongo_select(TicketFiles, start_page=1, items_count=100, ticket_id=ticket_id)]
    }
