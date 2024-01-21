from django.urls import include, path
from rest_framework_mongoengine.routers import DefaultRouter as MongoDefaultRouter

from . import views

router = MongoDefaultRouter()

router.register(
    'video_widgets',
    views.VideoWidgetViewSet,
    basename='video_widgets'
)

router.register(
    r'^video_widgets/(?P<widget_id>[a-zA-Z0-9_]{1,30})/videos',
    views.VideoViewSet,
    basename='videos'
)

router.register(
    (
        r'^video_widgets/(?P<widget_id>[a-zA-Z0-9_]{1,30})/videos/'
        r'(?P<video_id>[a-zA-Z0-9_]{1,30})/buttons'
    ),
    views.ButtonViewSet,
    basename='buttons'
)

urlpatterns = [
    path('', include(router.urls)),
]
