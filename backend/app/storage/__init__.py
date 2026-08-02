"""Minimal S3-compatible object storage client.

No-ops (logs and returns None) when S3 isn't configured — the same
graceful-degradation pattern used for Sentry, the LLM provider keys, and
email/SMTP elsewhere in this app. Works against real AWS S3 or any
S3-compatible endpoint (MinIO, DigitalOcean Spaces, etc.) via
S3_ENDPOINT_URL.
"""
from __future__ import annotations

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from app.core.config import settings
from app.core.logging import logger


def is_configured() -> bool:
    return bool(settings.S3_ACCESS_KEY and settings.S3_SECRET_KEY)


def _client():
    return boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT_URL or None,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION,
    )


def upload_bytes(key: str, data: bytes, content_type: str = "application/octet-stream") -> str | None:
    """Uploads `data` to `key` in the configured bucket.

    Returns the key on success, or None if S3 isn't configured (logged, not
    raised) so callers can proceed without object storage in local dev/CI.
    Raises on a real S3 error (bad credentials, bucket missing, network
    failure) so the caller/task can retry or surface the failure.
    """
    if not is_configured():
        logger.info("S3 not configured; skipping upload of %s.", key)
        return None

    try:
        _client().put_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=key,
            Body=data,
            ContentType=content_type,
        )
    except (BotoCoreError, ClientError):
        logger.exception("Failed to upload %s to S3 bucket %s.", key, settings.S3_BUCKET_NAME)
        raise

    logger.info("Uploaded %s to S3 bucket %s (%d bytes).", key, settings.S3_BUCKET_NAME, len(data))
    return key


def get_object_stream(key: str):
    """Fetches `key` from the configured bucket for streaming back to a
    client without loading the whole file into memory.

    Returns (body_stream, content_type, content_length), where body_stream
    is a botocore StreamingBody (iterate with `.iter_chunks()`). Returns
    None if S3 isn't configured, or if the key doesn't exist in the bucket
    (both are "nothing to stream" cases the caller should turn into a
    clear 503/404 rather than a raw boto3 traceback). Re-raises any other
    S3 error (bad credentials, network failure, etc).
    """
    if not is_configured():
        logger.info("S3 not configured; cannot download %s.", key)
        return None

    try:
        obj = _client().get_object(Bucket=settings.S3_BUCKET_NAME, Key=key)
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code", "")
        if error_code in ("NoSuchKey", "404"):
            logger.warning("Requested object %s not found in bucket %s.", key, settings.S3_BUCKET_NAME)
            return None
        logger.exception("Failed to download %s from S3 bucket %s.", key, settings.S3_BUCKET_NAME)
        raise
    except BotoCoreError:
        logger.exception("Failed to download %s from S3 bucket %s.", key, settings.S3_BUCKET_NAME)
        raise

    content_type = obj.get("ContentType", "application/octet-stream")
    content_length = obj.get("ContentLength")
    return obj["Body"], content_type, content_length
