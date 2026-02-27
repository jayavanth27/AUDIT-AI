"""Simple wrapper around AWS S3 operations used by the project."""

import uuid
from typing import BinaryIO

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from app.config import settings


s3_client = boto3.client("s3", region_name=settings.AWS_REGION)


def upload_fileobj(file_obj: BinaryIO, content_type: str, bucket: str = None) -> str:
    """Uploads file-like object to S3 and returns the object key."""
    bucket = bucket or settings.AWS_S3_BUCKET
    key = f"documents/{uuid.uuid4()}"
    try:
        s3_client.upload_fileobj(
            Fileobj=file_obj,
            Bucket=bucket,
            Key=key,
            ExtraArgs={"ContentType": content_type, "ACL": "private"},
        )
        return key
    except (BotoCoreError, ClientError) as e:
        raise


def generate_presigned_url(key: str, expires_in: int = 3600) -> str:
    """Return a presigned URL for the given object key.

    The URL is valid for `expires_in` seconds.
    """
    bucket = settings.AWS_S3_BUCKET
    return s3_client.generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expires_in
    )
