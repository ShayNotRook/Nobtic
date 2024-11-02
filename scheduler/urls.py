from django.urls import path, include


urlpatterns = [
    path('api/', include('scheduler.api.api_urls')),
]