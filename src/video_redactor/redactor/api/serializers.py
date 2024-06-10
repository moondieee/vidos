from rest_framework_mongoengine import serializers as mongoserializers
from rest_framework import serializers

from core.shortcuts import get_object_or_404
from ..models import Button, Video, VideoWidget
from ..utils import get_video_from_widget


class ButtonSerializer(mongoserializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Button
        fields = (
            'id',
            'type',
            'name',
            'video_id',
            'form_url',
            'redirect_url',
            'callback_url',
        )
        read_only_fields = (
            'id',
        )

    def create(self, validated_data):
        request = self.context['request']
        kwargs = self.context['view'].kwargs

        widget = get_object_or_404(
            VideoWidget,
            user_id=request.user.id,
            id=kwargs.get('widget_id')
        )
        video = get_video_from_widget(
            widget,
            kwargs.get('video_id')
        )
        button = super().create(validated_data)
        # MongoDB EmbeddedDocument add by append method
        video.buttons.append(button)

        # Saving all Mongo Document with EmbeddedDocuments
        widget.save()
        return button


class VideoSerializer(mongoserializers.EmbeddedDocumentSerializer):
    buttons = ButtonSerializer(
        many=True,
        required=False,
        read_only=True
    )

    class Meta:
        model = Video
        fields = (
            'id',
            'name',
            'video_url',
            'preview_img_url',
            'preview_img_jpeg_url',
            'buttons',
        )
        read_only_fields = (
            'id',
            'video_url',
            'preview_img_url',
            'preview_img_jpeg_url',
            'buttons',
        )

    def create(self, validated_data):
        request = self.context['request']
        kwargs = self.context['view'].kwargs

        # Get the widget that should have this created video
        widget = get_object_or_404(
            VideoWidget,
            user_id=request.user.id,
            id=kwargs.get('widget_id')
        )
        video = super().create(validated_data)
        # MongoDB EmbeddedDocument add by append method
        widget.videos.append(video)
        widget.save()
        return video


class VideoWidgetSerializer(mongoserializers.DocumentSerializer):
    videos = VideoSerializer(
        many=True,
        read_only=True
    )
    created = serializers.DateTimeField(
        source='id.generation_time',
        read_only=True
    )

    class Meta:
        model = VideoWidget
        fields = (
            'id',
            'website_id',
            'user_id',
            'videos',
            'created',
        )
        read_only_fields = (
            'id',
            'user_id',
            'videos',
            'created',
        )
