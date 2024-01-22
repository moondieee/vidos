from fastapi import HTTPException

from core.database import PyObjectId, video_widgets


async def get_widget_by_id(widget_id: str) -> dict:
    if widget := await video_widgets.find_one({'_id': PyObjectId(widget_id)}):
        # TODO Fix do it better through the Pydantic model
        # Pydantic model return '_id' and not a 'id' with Mongo ObjectId
        widget['id'] = str(widget['_id'])
        return widget

    raise HTTPException(status_code=404, detail='Widget not found')
