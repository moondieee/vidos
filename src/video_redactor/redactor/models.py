"""
Video widgets models by using BongoDB.
"""
from mongoengine import Document, EmbeddedDocument, fields

TYPE_CHOICES = [
    'VIDEO', 'REDIRECT', 'CONTACT_FORM', 'CALLBACK'
]


class Button(EmbeddedDocument):
    id = fields.SequenceField(
        primary_key=True,
        sequence_name='button_id_sequence'
    )
    type = fields.StringField(
        required=True,
        choices=TYPE_CHOICES
    )
    name = fields.StringField(
        required=True,
        default=None
    )
    video_id = fields.IntField(
        default=None
    )
    form_url = fields.StringField(
        default=None
    )
    redirect_url = fields.StringField(
        default=None
    )
    callback_url = fields.StringField(
        default=None
    )


class Video(EmbeddedDocument):
    id = fields.SequenceField(
        primary_key=True,
        sequence_name='video_id_sequence'
    )
    name = fields.StringField(
        default=None
    )
    video_url = fields.StringField(
        default=None
    )
    preview_img_url = fields.StringField(
        default=None
    )
    preview_img_jpeg_url = fields.StringField(
        default=None
    )
    buttons = fields.EmbeddedDocumentListField(
        Button
    )


class VideoWidget(Document):
    website_id = fields.IntField()
    user_id = fields.IntField()
    videos = fields.EmbeddedDocumentListField(
        Video
    )

    meta = {
        # The default name is incorrect (video_widget)
        'collection': 'video_widgets'
    }
