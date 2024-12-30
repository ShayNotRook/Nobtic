from django.urls import path, include

from .views import Login

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('api/', include('users.api.api_urls'))
]