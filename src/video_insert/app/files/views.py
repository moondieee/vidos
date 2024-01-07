from fastapi import APIRouter, Depends, status

from app.auth.auth import auth
from app.files.schemas import FileUpload, FileUploadResponse
from app.files.services import upload_file
from core.schemas import ExceptionModel
from .permissions import is_owner
from .services import get_filename, update_video_url

file_router = APIRouter(prefix='/files', tags=['files'])

@file_router.post(
    '/',
    response_model=FileUploadResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {'model': ExceptionModel},
        status.HTTP_404_NOT_FOUND: {'model': ExceptionModel},
    },
    tags=['files'],
    dependencies=[Depends(is_owner)]
)
async def file_upload(
    filename: str = Depends(get_filename),
    file: FileUpload = Depends(),
    user: dict = Depends(auth)
):
    file.file.filename = filename
    if uploaded := await upload_file(file=file.file):
        await update_video_url(file, uploaded.get('url'))
        return uploaded
