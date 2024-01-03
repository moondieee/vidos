from fastapi import UploadFile

from app.files.client import MinioClient
from core.settings import settings


async def upload_file(
    file: UploadFile
) -> dict | None:
    client = MinioClient(
        endpoint=f'{settings.MINIO_HOST}:{settings.MINIO_PORT}',
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        bucket_name=settings.MINIO_BUCKET_NAME
    )
    client.upload_file(file=file)
    return {'filename': file.filename}
