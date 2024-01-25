import logging
import uuid
from io import BytesIO

import cv2
from bson import ObjectId
from fastapi import HTTPException, UploadFile

from core.database import video_widgets
from core.media_storage import client as minio_client
from core.media_storage import minio_endpoint
from core.settings import settings

logger = logging.getLogger(__name__)


async def upload_video_previews(
    video_url: str,
    user_id: str | int
) -> tuple[str, str]:
    """
    Create and upload two previews (JPEG and WebP) to MinIO.

    :param video_url: The location of the video used for creating previews.
    :param user_id: User ID for inserting into the user directory.

    :return: A tuple containing two URLs for the uploaded previews (JPEG and WebP).
    """
    # TODO init video by video: UploadFile variable
    # Download firts frame of video for preview
    cap = cv2.VideoCapture(video_url)
    success, frame = cap.read()

    if not success:
        error_msg = 'Invalid video to get preview. Destination of video - {video_url}'
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Creating images jpg and webp
    _, jpeg_image = cv2.imencode(".jpg", frame)
    _, webp_image = cv2.imencode(".webp", frame)

    # Directory for previews of widget videos
    directory = f'{user_id}/video_widgets/previews/'
    # Generate UUIDs for filenames
    jpeg_bytesio = BytesIO(jpeg_image.tobytes())
    webp_bytesio = BytesIO(webp_image.tobytes())

    jpeg_filename = directory + str(uuid.uuid4()) + '.jpg' + 'test'
    webp_filename = directory + str(uuid.uuid4()) + '.webp'

    # Upload jpeg and webp preview to Minio storage
    minio_client.client.put_object(
        settings.MINIO_BUCKET_NAME,
        jpeg_filename,
        data=jpeg_bytesio,
        length=len(jpeg_image.tobytes()),
        content_type='image/jpeg'
    )
    minio_client.client.put_object(
        settings.MINIO_BUCKET_NAME,
        webp_filename,
        data=webp_bytesio,
        length=len(webp_image.tobytes()),
        content_type='image/webp'
    )
    # TODO GET urls better
    scheme = 'https://' if settings.MINIO_SECURE else 'http://'
    jpeg_url = f'{scheme}{minio_endpoint}/{settings.MINIO_BUCKET_NAME}/{jpeg_filename}'
    webp_url = f'{scheme}{minio_endpoint}/{settings.MINIO_BUCKET_NAME}/{webp_filename}'
    return jpeg_url, webp_url


async def upload_video(
    video: UploadFile,
    user_id: str | int
) -> str:
    """
    Uploads a video to the media storage and returns a link to the uploaded video.

    :param video: The video file to be uploaded.
    :param user_id: User ID for organizing the storage.

    :return: a str with URL of the uploaded video.
    """
    # Change filename to almost unique filename with a video format
    video.filename = str(uuid.uuid4()) + video.filename.split('.')[-1]

    # Directory for widget videos
    directory = f'{user_id}/video_widgets/videos'
    result = minio_client.upload_file(
        file=video,
        directory=directory
    )
    await upload_video_previews(result.location, user_id)
    return result.location


async def update_video_url(
    video_url: str,
    widget_id: str,
    video_id: int
) -> dict:
    """
    Обновление видео url в схеме виджета.
    """
    filter_query = {
        '_id': ObjectId(widget_id),
        'videos._id': int(video_id)
    }
    update_query = {
        '$set': {
            'videos.$[v].video_url': video_url
        }
    }
    array_filters = [{'v._id': int(video_id)}]
    try:
        updated_widget = await video_widgets.find_one_and_update(
            filter_query,
            update_query,
            array_filters=array_filters,
            return_document=True
        )

        # init video schema
        # add id: int in video and in buttons
        updated_video: dict = {}
        for video in updated_widget['videos']:
            if video['_id'] == video_id:
                updated_video = video
                # Add id: int from _id: int
                updated_video['id'] = int(updated_video['_id'])
                break
        for button in updated_video['buttons']:
            # Add id: int from _id: int
            button['id'] = int(button['_id'])

        return updated_video
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
