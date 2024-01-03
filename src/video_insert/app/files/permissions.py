from bson import ObjectId
from fastapi import Depends, HTTPException, status

from app.auth.auth import auth
from app.files.schemas import FileUpload
from core.database import video_widgets


async def is_owner(file: FileUpload = Depends(), user: dict = Depends(auth)):
    if await video_widgets.find_one(
        {
            '_id': ObjectId(file.video_widget_id),
            'user_id': user.get('id')
        }
    ):
        return True

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail='Access forbidden'
    )
