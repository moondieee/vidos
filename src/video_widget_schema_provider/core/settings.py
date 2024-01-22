import os
from functools import lru_cache
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings, root_validator

load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    APP_TITLE: str = os.getenv('APP_TITLE', 'Public stories schema provider')
    TEMP_FOLDER: str = os.getenv('TEMP_FOLDER', 'temp')
    TIME_ZONE: str = os.getenv('TIME_ZONE', 'UTC')

    MONGO_INITDB_ROOT_USERNAME: str = os.getenv('MONGO_INITDB_ROOT_USERNAME', 'username')
    MONGO_INITDB_ROOT_PASSWORD: str = os.getenv('MONGO_INITDB_ROOT_PASSWORD', 'password')
    MONGO_HOST: str = os.getenv('MONGO_HOST', 'mongodb')
    MONGO_PORT: int = int(os.getenv('MONGO_PORT', '27017'))
    MONGO_URI: str = None
    MONGO_DATABASE: str = os.getenv('MONGO_DATABASE', 'video_widgets')

    @root_validator
    def uri_validator(cls, values) -> dict:
        values['MONGO_URI'] = (
            f'mongodb://{values["MONGO_INITDB_ROOT_USERNAME"]}:{values["MONGO_INITDB_ROOT_PASSWORD"]}'
            f'@{values["MONGO_HOST"]}:{values["MONGO_PORT"]}'
        )
        return values


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
