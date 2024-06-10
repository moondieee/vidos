from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# All API docs in video widget scheme
schema_view = get_schema_view(
    openapi.Info(
        title='video_redactor',
        default_version='v1',
        description='video_redactor service doc',
        terms_of_service='No',
        contact=openapi.Contact(
            name='Andreev Aisen',
            email='isenandreev@gmail.com'
        ),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Swagger doc
    path(
        'video_redactor/swagger/',
        schema_view.with_ui(
            'swagger',
            cache_timeout=0
        ),
        name='schema-swagger-ui'
    ),
    path(
        'video_redactor/redoc/',
        schema_view.with_ui(
            'redoc',
            cache_timeout=0
        ),
        name='schema-redoc'
    ),

    # API
    path('api/v1/video_redactor/', include('redactor.api.urls'))
]

urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
