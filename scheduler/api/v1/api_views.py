from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import viewsets
from rest_framework import permissions

from django.contrib.auth.decorators import login_required

from scheduler.models import Salon, Service

from .serializers import ServiceSerializer, SalonSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        salon = Salon.objects.get(owner=self.request.user)
        return Service.objects.filter(salon=salon)
    

class SalonRetrieve(RetrieveAPIView):
    serializer_class = SalonSerializer
    
    def get_queryset(self):
        return Salon.objects.get(owner=self.request.user)