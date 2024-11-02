from django.urls import path, include

from .api_views import ServiceViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'services', ServiceViewSet, basename='service')


urlpatterns = [
    path('', include(router.urls)),
]
