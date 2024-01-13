"""
Video widgets models by using BongoDB.
"""
from bson import ObjectId

from mongoengine import Document, EmbeddedDocument, fields


class Button(EmbeddedDocument):
    id = fields.ObjectIdField(
        required=True,
        default=ObjectId
    )
    type = fields.StringField(
        required=True
    )
    name = fields.StringField(
        required=True,
        default=None
    )
    video_id = fields.IntField(
        default=None
    )


class Video(EmbeddedDocument):
    id = fields.ObjectIdField(
        required=True,
        default=ObjectId
    )
    name = fields.StringField(
        default=None
    )
    video_url = fields.StringField(
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
