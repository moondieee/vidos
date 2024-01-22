from asyncio import create_task
from contextlib import asynccontextmanager
from shutil import rmtree

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.health import mongodb_health
from core.routers import api_router
from core.schemas import HealthModel
from core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    rmtree(settings.TEMP_FOLDER, ignore_errors=True)


app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)

app.include_router(api_router)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('api/v1/video_widget_schema/', response_model=HealthModel, tags=['health'])
async def health_check():
    mongodb_task = create_task(mongodb_health())
    mongodb = await mongodb_task
    return {'api': True, 'mongodb': mongodb}
