import logging

from datetime import datetime

from fastapi import Depends, HTTPException, UploadFile

from app.auth.auth import auth
from app.files.schemas import FileUpload
from app.files.client import MinioClient
from core.database import video_widgets
from core.settings import settings

logger = logging.getLogger(__name__)


async def upload_file(
    file: UploadFile
) -> dict | None:
    
    minio_endpoint = f'{settings.MINIO_HOST}:{settings.MINIO_PORT}'
    client = MinioClient(
        endpoint=minio_endpoint,
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        bucket_name=settings.MINIO_BUCKET_NAME
    )

    client.upload_file(file=file)
    
    protocol = "https" if settings.MINIO_SECURE else "http"
    file_url = (
        f'{protocol}://'
        + f'{settings.MINIO_HOST}:'
        + f'{settings.MINIO_PORT}/'
        + f'{settings.MINIO_BUCKET_NAME}/'
        + f'{file.filename}'
    )

    return {
        'filename': file.filename,
        'url': file_url
    }


async def update_video_url(
    file: FileUpload, file_url: str
) -> None:
    filter_query = {
        '_id': file.video_widget_id,
        'videos.id': file.video_id
    }

    existing_video = await video_widgets.find_one(filter_query)

    if existing_video:
        update_query = {
            '$set': {
                f'videos.$[v].video_url': file_url
            }
        }
        array_filters = [{'v.id': file.video_id}]

        try:
            await video_widgets.update_one(
                filter_query,
                update_query,
                array_filters=array_filters
            )
        except Exception as err:
            detail = 'Error updating URL of video in video widget'
            logger.error(
                '%s. %s',
                detail,
                err
            )
            raise HTTPException(
                status_code=400,
                detail='Error updating URL of video in video widget'
            )
    else:
        raise HTTPException(
            status_code=400,
            detail='Video with specified video_widget_id or video_id does not exist'
        )


async def get_filename(
    file: FileUpload = Depends(), user: int = Depends(auth)
) -> str:
    date = str(datetime.utcnow().strftime('%Y-%m-%d'))
    video_identification = f'{file.video_widget_id}_{file.video_id}_video'
    format = file.file.filename.split('.')[-1]
    filename = f'{date}_{video_identification}_{user.get("id")}.{format}'
    return filename
