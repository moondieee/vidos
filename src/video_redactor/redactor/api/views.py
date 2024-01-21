from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet

from core.shortcuts import get_object_or_404
from .serializers import (ButtonSerializer, VideoWidgetSerializer,
                          VideoSerializer)
from ..models import VideoWidget
from ..utils import get_video_from_widget


class VideoWidgetViewSet(MongoModelViewSet):
    serializer_class = VideoWidgetSerializer

    def get_queryset(self):
        return VideoWidget.objects.filter(
            user_id=self.request.user.id
        )

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class VideoViewSet(MongoModelViewSet):
    serializer_class = VideoSerializer

    def get_queryset(self):
        widget = get_object_or_404(
            VideoWidget,
            user_id=self.request.user.id,
            id=self.kwargs.get('widget_id')
        )
        return widget.videos


class ButtonViewSet(MongoModelViewSet):
    serializer_class = ButtonSerializer

    def get_queryset(self):
        widget = self.get_widget()
        video = get_video_from_widget(
            widget,
            self.kwargs.get('video_id')
        )
        return video.buttons

    def get_widget(self):
        return get_object_or_404(
            VideoWidget,
            user_id=self.request.user.id,
            id=self.kwargs.get('widget_id')
        )
