from django.urls import path, include

from .views import all_apps

app_name = 'scheduler'

urlpatterns = [
    # API Views
    path('api/', include('scheduler.api.api_urls')),
    # Basic Views
    path('apps/', all_apps, name='apps')   
]