import uuid
from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime

import boto3
from botocore import exceptions as botocore_exceptions
from fastapi import HTTPException

from burrito.models.m_ticket_files import TicketFiles
from burrito.utils.config_reader import get_config
from burrito.utils.logger import get_logger
from burrito.utils.mongo_util import mongo_delete, mongo_insert

client = boto3.client('s3')


def upload_file(ticket_id: int, file_owner_id: int, file_name: str, file: bytes, content_type: str | None) -> str:
    file_id = f"{ticket_id}/{datetime.now().date()}/{uuid.uuid4().hex[:8]}_{file_name}"
    encoded_file_id = urlsafe_b64encode(file_id.encode()).decode()

    try:
        client.put_object(
            Body=file,
            Bucket=get_config().BURRITO_FILES_BUCKET_NAME,
            Key=file_id
        )
    except botocore_exceptions.ClientError as exc:
        get_logger().critical(f"Failed to upload file '{file_id}' to s3")
        get_logger().critical(exc)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file '{file_id}'"
        ) from exc

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

    except botocore_exceptions.ClientError as exc:
        get_logger().critical(f"Failed to download file '{file_id}' from s3")
        get_logger().critical(exc)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to download file '{file_id}'"
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=403,
            detail=f"File with file_id {file_id} is not exists"
        ) from exc


def delete_file(file_id: str):
    file_id_decoded = urlsafe_b64decode(file_id).decode()

    try:
        client.delete_object(
            Bucket=get_config().BURRITO_FILES_BUCKET_NAME,
            Key=file_id_decoded
        )
        mongo_delete(TicketFiles, file_id=file_id)

    except botocore_exceptions.ClientError as exc:
        get_logger().critical(f"Failed to delete file '{file_id_decoded}' from s3")
        get_logger().critical(exc)
        raise HTTPException(
            status_code=403,
            detail=f"Failed to delete file '{file_id_decoded}'"
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=403,
            detail=f"File with file_id {file_id} is not exists"
        ) from exc
