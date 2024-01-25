from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet

from .serializers import (ButtonSerializer, VideoWidgetSerializer,
                          VideoSerializer)
from ..models import VideoWidget
from ..utils import get_video_from_widget, get_widget_or_404


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
        self.widget = get_widget_or_404(
            self.request.user.id,
            self.kwargs.get('widget_id')
        )
        return self.widget.videos

    # Video is updated only after saving a widget
    def perform_update(self, serializer):
        serializer.save()
        self.widget.save()

    def perform_destroy(self, instance):
        widget = get_widget_or_404(
            self.request.user.id,
            self.kwargs.get('widget_id')
        )
        widget.videos.remove(instance)
        widget.save()


class ButtonViewSet(MongoModelViewSet):
    serializer_class = ButtonSerializer

    def get_queryset(self):
        self.widget = get_widget_or_404(
            self.request.user.id,
            self.kwargs.get('widget_id')
        )
        video = get_video_from_widget(
            self.widget,
            self.kwargs.get('video_id')
        )
        return video.buttons

    # Video is updated only after saving a widget
    def perform_update(self, serializer):
        serializer.save()
        self.widget.save()

    def perform_destroy(self, instance):
        widget = get_widget_or_404(
            self.request.user.id,
            self.kwargs.get('widget_id')
        )
        video = get_video_from_widget(
            widget,
            self.kwargs.get('video_id')
        )
        video.buttons.remove(instance)
        widget.save()
