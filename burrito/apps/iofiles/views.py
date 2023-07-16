from typing import Annotated
from pathlib import Path

from fastapi import Depends, Form, UploadFile

import aiofiles

from burrito.models.tickets_model import Tickets

from burrito.utils.auth import get_auth_core, BurritoJWT
from burrito.utils.tickets_util import is_ticket_exist


async def iofiles__upload_file_for_ticket(
    ticket_id: Annotated[int, Form(...)],
    file_list: list[UploadFile],
    __auth_obj: BurritoJWT = Depends(get_auth_core())
):
    await __auth_obj.verify_access_token()

    ticket: Tickets | None = is_ticket_exist(ticket_id)

    for file_item in file_list:
        path_to_file: Path = Path("storage") / file_item.filename
        async with aiofiles.open(
            path_to_file,
            mode="w"
        ) as file:
            for line in file_item.file:
                await file.write(line.decode("utf-8"))


#    await get_file_manager().push_files(deepcopy(file_list))
