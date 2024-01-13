"""
Utilities for working with Django, mongoengine, and related functionalities.
"""

from django.http import Http404

from .models import VideoWidget, Video


def get_video_from_widget(widget: VideoWidget, video_id: str) -> Video:
    """
    Retrieve a video from a VideoWidget based on the given video_id.

    Args:
        widget (VideoWidget): The VideoWidget instance.
        video_id (str): The ID of the video to retrieve.

    Returns:
        Video: EmbeddedDocument Video instance.

    Raises:
        Http404: If the specified video_id is not found within the VideoWidget.
    """
    video = next(
        (v for v in widget.videos if str(v.id) == video_id),
        None
    )

    if video is None:
        raise Http404('Video not found.')

    return video
