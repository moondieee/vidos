from typing import Any, Dict

from fastapi import HTTPException

from core.database import PyObjectId, video_widgets


async def convert_widget_data(widget: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert MongoDB data to the desired format.

    Args:
        widget: MongoDB data for the widget.
    """
    widget['id'] = str(widget['_id'])

    for video in widget['videos']:
        video['id'] = int(video['_id'])
        for button in video['buttons']:
            button['id'] = int(button['_id'])

    return widget


async def get_widget_by_id(widget_id: str) -> dict:
    if widget := await video_widgets.find_one({'_id': PyObjectId(widget_id)}):
        # TODO fix it more delicately. Through models
        converted_widget = await convert_widget_data(widget)
        return converted_widget

    raise HTTPException(status_code=404, detail='Widget not found')
