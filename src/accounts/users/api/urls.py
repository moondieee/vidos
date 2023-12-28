from django.urls import include, path

from . import views

urlpatterns = [
    path('users/me/', views.UserMeAPIView.as_view()),
    path('', include('djoser.urls.authtoken')),
]
