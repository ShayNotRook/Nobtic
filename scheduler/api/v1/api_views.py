from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.decorators import login_required

from scheduler.models import Salon, Service, AppointmentSlot, Appointment

from .serializers import ServiceSerializer, SalonSerializer, AppSlotSerializer, AppointmentSerializer


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
    
    

class AppSlotViewSet(viewsets.ModelViewSet):
    serializer_class = AppSlotSerializer
    permissions = [IsAuthenticated]
    
    
    def get_queryset(self):
        return AppointmentSlot.objects.filter(salon__owner=self.request.user)
    
    # def retrieve(self, request, id: int, *args, **kwargs):
    #     return AppointmentSlot.objects.filter(id=id, salon__owner=self.request.user)
    
    
    
class AppViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self, **kwargs):
        appointment_slot_id = self.kwargs.get('appointment_slot_id')
        if appointment_slot_id:
            return Appointment.objects.filter(slot__id=appointment_slot_id, slot__salon__owner=self.request.user)
    
        return Appointment.objects.none()