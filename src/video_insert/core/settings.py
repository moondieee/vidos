import os
from functools import lru_cache
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings, root_validator

load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    APP_TITLE: str = os.getenv('APP_TITLE', 'video insert')
    ADMIN_USERNAME: str = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD: str = os.getenv('ADMIN_PASSWORD', 'admin')
    ADMIN_EMAIL: str = os.getenv('ADMIN_EMAIL', 'admin@admin.admin')
    TEMP_FOLDER: str = os.getenv('TEMP_FOLDER', 'temp')
    TIME_ZONE: str = os.getenv('TIME_ZONE', 'UTC')

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'SECRET_KEY')
    ALGORITHM: str = os.getenv('HS256', 'HS256')

    MONGO_INITDB_ROOT_USERNAME: str = os.getenv('MONGO_INITDB_ROOT_USERNAME', 'username')
    MONGO_INITDB_ROOT_PASSWORD: str = os.getenv('MONGO_INITDB_ROOT_PASSWORD', 'password')
    MONGO_HOST: str = os.getenv('MONGO_HOST', 'mongodb')
    MONGO_PORT: int = int(os.getenv('MONGO_PORT', '27017'))
    MONGO_URI: str = None

    MINIO_ROOT_USER: str = os.getenv('MINIO_ROOT_USER', 'username')
    MINIO_ROOT_PASSWORD: str = os.getenv('MINIO_ROOT_PASSWORD', 'password')
    MINIO_HOST: str = os.getenv('MINIO_HOST', 'password')
    MINIO_PORT: int = int(os.getenv('MINIO_PORT', 9000))
    MINIO_SECURE: bool = True if os.getenv('MINIO_SECURE') == 'True' else False
    MINIO_BUCKET_NAME: str = os.getenv('MINIO_BUCKET_NAME', 'minio-bucket')
    MINIO_URI: str = None

    # Backend services urls
    AUTH_SERVICE_URL = "http://localhost:8000"

    # Videos
    MAX_VIDEO_SIZE_MB = int(os.getenv('MAX_VIDEO_SIZE_MB', '50'))

    @root_validator
    def uri_validator(cls, values) -> dict:
        values['MONGO_URI'] = (
            f'mongodb://{values["MONGO_INITDB_ROOT_USERNAME"]}:{values["MONGO_INITDB_ROOT_PASSWORD"]}'
            f'@{values["MONGO_HOST"]}:{values["MONGO_PORT"]}'
        )
        values['MINIO_URI'] = f'{values["MINIO_HOST"]}:{values["MINIO_PORT"]}'
        return values


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
