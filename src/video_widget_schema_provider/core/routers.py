from fastapi import APIRouter

from app.widgets.views import widget_router

api_router = APIRouter(prefix='/api/v1/video_widget_schema')

api_router.include_router(widget_router)
