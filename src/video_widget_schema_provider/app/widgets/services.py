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

        # Replace values in video_url, preview_img_url, and preview_img_jpeg_url
        if video.get('video_url'):
            video['video_url'] = video['video_url'].replace("minio:9000", "localhost:3000")
        if video.get('preview_img_url'):
            video['preview_img_url'] = video['preview_img_url'].replace("minio:9000", "localhost:3000")
        if video.get('preview_img_jpeg_url'):
            video['preview_img_jpeg_url'] = video['preview_img_jpeg_url'].replace("minio:9000", "localhost:3000")

        for button in video['buttons']:
            button['id'] = int(button['_id'])

    return widget


async def get_widget_by_id(widget_id: str) -> dict:
    if widget := await video_widgets.find_one({'_id': PyObjectId(widget_id)}):
        # TODO fix it more delicately. Through models
        converted_widget = await convert_widget_data(widget)
        return converted_widget

    raise HTTPException(status_code=404, detail='Widget not found')
