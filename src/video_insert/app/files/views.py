from fastapi import APIRouter, Depends, Path, status

from app.auth.auth import auth
from app.files.schemas import VideoUpload, Video
from app.files.services import update_video_url, upload_video, upload_video_previews
from core.schemas import ExceptionModel

from .permissions import is_existing_video, is_owner

video_router = APIRouter(prefix='/video_widget', tags=['videos'])


@video_router.post(
    '/{widget_id}/video/{video_id}/',
    response_model=Video,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {'model': ExceptionModel},
        status.HTTP_404_NOT_FOUND: {'model': ExceptionModel},
    },
    tags=['videos'],
    dependencies=[Depends(is_owner), Depends(is_existing_video)]
)
async def video_upload(
    widget_id: str = Path(..., title='Widget ID'),
    video_id: int = Path(..., title='Video ID'),

    # filename: str = Depends(get_filename),
    file: VideoUpload = Depends(),
    user: dict = Depends(auth)
):
    if video_url := await upload_video(
        file.file,
        user['id']
    ):
        preview_jpeg, preview_webp = await upload_video_previews(
            video_url,
            user['id']
        )
        if video_schema := await update_video_url(
            video_url=video_url,
            widget_id=widget_id,
            video_id=video_id,
            preview_jpeg_url=preview_jpeg,
            preview_webp_url=preview_webp,
        ):
            return video_schema
