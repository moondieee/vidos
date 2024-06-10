from fastapi import APIRouter, Path, status

from app.widgets.schemas import VideoWidget
from app.widgets.services import get_widget_by_id
from core.schemas import ExceptionModel

widget_router = APIRouter()


@widget_router.get(
    '/{widget_id}/',
    response_model=VideoWidget,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {'model': ExceptionModel},
    },
)
async def read_widget_schema(widget_id: str = Path(..., title='The ID of the widget to retrieve')):
    if widget := await get_widget_by_id(widget_id):
        return widget
