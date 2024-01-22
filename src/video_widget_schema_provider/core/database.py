import pymongo
from bson import ObjectId
from motor import motor_asyncio

from core.settings import settings

# Async MongoDB client
client = motor_asyncio.AsyncIOMotorClient(
    settings.MONGO_URI, serverSelectionTimeoutMS=10000
)
db = client.database

video_widgets = db.get_collection('video_widgets')


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')
