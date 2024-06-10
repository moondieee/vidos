from fastapi import APIRouter

from app.files.views import video_router

api_router = APIRouter(prefix='/api/v1/video_insert')

api_router.include_router(video_router)
