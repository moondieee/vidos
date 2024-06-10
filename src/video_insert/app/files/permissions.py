from bson import ObjectId
from fastapi import Depends, HTTPException, Path, status

from app.auth.auth import auth
from core.database import PyObjectId, video_widgets


async def is_owner(
    widget_id: str = Path(..., title='Widget ID'),
    user: dict = Depends(auth)
):
    if not ObjectId.is_valid(widget_id):
        raise HTTPException(
            status_code=404,
            detail='video_widget does not exist'
        )

    if not await video_widgets.find_one(
        {
            '_id': PyObjectId(widget_id),
            'user_id': user.get('id')
        }
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Access forbidden'
        )


async def is_existing_video(
    widget_id: str = Path(..., title='Widget ID'),
    video_id: int = Path(..., title='Video ID')
):
    if (
        not ObjectId.is_valid(widget_id)
        or not await video_widgets.find_one(
            {
                '_id': PyObjectId(widget_id)
            }
        )
    ):
        raise HTTPException(
            status_code=404,
            detail='video_widget does not exist'
        )

    if not await video_widgets.find_one(
        {
            '_id': ObjectId(widget_id),
            'videos._id': int(video_id)
        }
    ):
        raise HTTPException(
            status_code=404,
            detail='video does not exist'
        )
