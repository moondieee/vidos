from typing import List

from fastapi import HTTPException, UploadFile
from pydantic import BaseModel, validator

from app.files.utils import form_body
from core.settings import settings


@form_body
class VideoUpload(BaseModel):
    file: UploadFile

    @validator('file')
    def check_file_type(cls, file: UploadFile):
        if not file.content_type.startswith('video'):
            raise HTTPException(status_code=400, detail='Uploaded file is not a video')

        return file

    @validator('file')
    def check_size_video(cls, file: UploadFile):
        max_video_size = (
            settings.MAX_VIDEO_SIZE_MB
            * 1024 * 1024
        )
        if file.size > max_video_size:
            raise HTTPException(status_code=400, detail='File size exceeds limit')

        return file


class Button(BaseModel):
    id: int
    type: str | None
    name: str | None
    video_id: int = None


class Video(BaseModel):
    id: int
    name: str | None
    video_url: str | None
    buttons: List[Button] | None
