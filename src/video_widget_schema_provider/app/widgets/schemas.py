from typing import List

from pydantic import BaseModel


class Button(BaseModel):
    id: int
    type: str | None
    name: str = None
    video_id: int = None


class Video(BaseModel):
    id: int
    name: str = None
    video_url: str = None
    buttons: List[Button] | None


class VideoWidget(BaseModel):
    id: str
    website_id: int | None
    user_id: int
    videos: List[Video] | None
