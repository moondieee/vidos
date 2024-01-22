from bson import ObjectId
from fastapi import HTTPException, UploadFile
from pydantic import BaseModel, validator

from app.files.utils import form_body
from core.database import sync_video_widgets
from core.settings import settings


@form_body
class FileUpload(BaseModel):
    file: UploadFile
    video_widget_id: str
    video_id: int

    @validator('video_id')
    def validate_video_id_exists(cls, video_id: int, values):
        if sync_video_widgets.find_one(
            {
                '_id': ObjectId(values.get('video_widget_id')),
                'videos': {
                    '$elemMatch': {
                        '_id': video_id
                    }
                }
            }
        ):
            return video_id

        raise HTTPException(
            status_code=400,
            detail='Video with specified video_widget_id or video_id does not exists'
        )

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


class FileUploadResponse(BaseModel):
    filename: str
    url: str

    class Config:
        json_encoders = {ObjectId: str}
