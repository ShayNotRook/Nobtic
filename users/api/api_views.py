from rest_framework import generics, permissions
from rest_framework.decorators import api_view

from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from .serializers import UserSerializer


User = get_user_model()

class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    
    def get_object(self):
        return self.request.user
    