from typing import Annotated

from bson.objectid import ObjectId
from funcy import chunks

from fastapi import Depends, Form, UploadFile, HTTPException
from fastapi.responses import StreamingResponse

from burrito.models.tickets_model import Tickets
from burrito.models.m_ticket_files import TicketFiles

from burrito.utils.auth import get_auth_core, BurritoJWT
from burrito.utils.tickets_util import (
    is_ticket_exist,
    create_ticket_file_action,
    am_i_own_this_ticket,
    create_ticket_action
)
from burrito.utils.query_util import STATUS_OPEN
from burrito.utils.mongo_util import mongo_save_file, mongo_get_file, mongo_select, mongo_delete_file
from burrito.utils.logger import get_logger


async def iofiles__upload_file_for_ticket(
    ticket_id: Annotated[int, Form(...)],
    file_list: list[UploadFile],
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload = await __auth_obj.require_access_token()

    ticket: Tickets | None = is_ticket_exist(ticket_id)

    if token_payload.user_id not in (ticket.creator.user_id, ticket.assignee.user_id if ticket.assignee else -1):
        raise HTTPException(
            status_code=403,
            detail="Is not allowed to attach files to this ticket"
        )

    file_ids = []
    for file_item in file_list:
        current_file_id = mongo_save_file(
            ticket.ticket_id,
            token_payload.user_id,
            file_item.filename,
            await file_item.read(),
            file_item.content_type
        )
        get_logger().info(
           f"User {token_payload.user_id} have uploaded file {current_file_id} ({file_item.size} bytes)"
        )
        file_ids.append(current_file_id)
        create_ticket_file_action(
            ticket_id=ticket.ticket_id,
            user_id=token_payload.user_id,
            value=file_item.filename,
            file_meta_action="upload"
        )

    if ticket.status.status_id in (4, 6) and am_i_own_this_ticket(ticket.creator.user_id, token_payload.user_id):
        create_ticket_action(
            ticket_id=ticket.ticket_id,
            user_id=token_payload.user_id,
            field_name="status",
            old_value=ticket.status.name,
            new_value=STATUS_OPEN.name
        )
        ticket.status = STATUS_OPEN
        ticket.save()

    return {
        "file_id": file_ids
    }


async def iofiles__get_file(
    file_id: str,
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload = await __auth_obj.require_access_token()

    file_data = mongo_select(TicketFiles, file_id=file_id)
    if not file_data:
        raise HTTPException(
            status_code=404,
            detail=f"File {file_id} is not exist"
        )
    file_data = TicketFiles(**file_data[0])

    ticket: Tickets | None = is_ticket_exist(file_data.ticket_id)

    if ticket.anonymous and token_payload.user_id not in (ticket.creator.user_id, ticket.assignee.user_id if ticket.assignee else -1):
        raise HTTPException(
            status_code=403,
            detail="Is not allowed to attach files to this ticket"
        )

    clear_filename = file_data.file_name.replace("\"", "")
    return StreamingResponse(
        content=(chunk for chunk in chunks(1024, mongo_get_file(file_id))),
        headers={
            "Content-Disposition": f'attachment; filename="{clear_filename}"',
        } | ({"Content-Type": file_data.content_type} if file_data.content_type else {})
    )


async def iofiles__get_file_ids(
    ticket_id: Annotated[int, Form(...)],
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload = await __auth_obj.require_access_token()

    ticket: Tickets | None = is_ticket_exist(ticket_id)

    if ticket.anonymous and token_payload.user_id not in (ticket.creator.user_id, ticket.assignee.user_id if ticket.assignee else -1):
        raise HTTPException(
            status_code=403,
            detail="Is not allowed to attach files to this ticket"
        )

    return {
        "file_ids": [TicketFiles(**item) for item in mongo_select(TicketFiles, start_page=1, items_count=100, ticket_id=ticket_id)]
    }


async def iofiles__delete_file(
    file_id: str = Form(...),
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    token_payload = await __auth_obj.require_access_token()

    file_data = mongo_select(TicketFiles, file_id=file_id)
    if not file_data:
        raise HTTPException(
            status_code=404,
            detail=f"File {file_id} is not exist"
        )
    file_data = TicketFiles(**file_data[0])

    ticket: Tickets | None = is_ticket_exist(file_data.ticket_id)

    if (
        (ticket.assignee and token_payload.user_id == ticket.assignee.user_id)
        or (token_payload.user_id == ticket.creator.user_id and token_payload.user_id == file_data.owner_id)
    ):
        file_data = mongo_select(
            TicketFiles,
            file_id=ObjectId(file_id)
        )
        if file_data:
            file_data = file_data[0]

        create_ticket_file_action(
            ticket_id=ticket.ticket_id,
            user_id=token_payload.user_id,
            value=file_data["file_name"] if file_data else "file",
            file_meta_action="delete"
        )
        mongo_delete_file(file_id)
        return

    raise HTTPException(
        status_code=403,
        detail="Is not allowed to delete files attached to this ticket"
    )
