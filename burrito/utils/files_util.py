import uuid
from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime

import boto3
from fastapi import HTTPException

from burrito.models.m_ticket_files import TicketFiles
from burrito.utils.config_reader import get_config
from burrito.utils.mongo_util import mongo_delete, mongo_insert

client = boto3.client('s3')


def upload_file(ticket_id: int, file_owner_id: int, file_name: str, file: bytes, content_type: str | None) -> str:
    file_id = f"{ticket_id}/{datetime.now().date()}/{uuid.uuid4().hex[:8]}_{file_name}"
    encoded_file_id = urlsafe_b64encode(file_id.encode()).decode()

    client.put_object(
        Body=file,
        Bucket=get_config().BURRITO_FILES_BUCKET_NAME,
        Key=file_id
    )

    if content_type is None:
        content_type = ""

    mongo_insert(
        TicketFiles(
            ticket_id=ticket_id,
            owner_id=file_owner_id,
            file_id=encoded_file_id,
            file_name=file_name,
            content_type=content_type
        )
    )

    return encoded_file_id


def download_file(file_id: str) -> bytes:
    file_id = urlsafe_b64decode(file_id).decode()

    try:
        response = client.get_object(
            Bucket=get_config().BURRITO_FILES_BUCKET_NAME,
            Key=file_id
        )
        return response["Body"].read()

    except Exception as exc:
        raise HTTPException(
            status_code=403,
            detail=f"File with file_id {file_id} is not exists"
        ) from exc


def delete_file(file_id: str):
    try:
        client.delete_object(
            Bucket=get_config().BURRITO_FILES_BUCKET_NAME,
            Key=urlsafe_b64decode(file_id).decode()
        )
        mongo_delete(TicketFiles, file_id=file_id)

    except Exception as exc:
        raise HTTPException(
            status_code=403,
            detail=f"File with file_id {file_id} is not exists"
        ) from exc
