from fastapi import APIRouter

from app.files.views import file_router

api_router = APIRouter(prefix='/api/v1/video_insert')

api_router.include_router(file_router)
