from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import viewsets
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from datetime import datetime

from scheduler.models import Salon, Service, AppointmentSlot, Appointment
from users.models import SalonEmployee

from .serializers import ServiceSerializer, SalonSerializer, AppSlotSerializer, AppointmentSerializer
from rest_framework.decorators import api_view, permission_classes


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
    
    

# @api_view(['GET'])
# def get_all_apps(request):
#     app_slots = AppointmentSlot.objects.filter(employee = request.user.salon_user)
    


class AppSlotViewSet(viewsets.ModelViewSet):
    serializer_class = AppSlotSerializer
    permission_classes = [IsAuthenticated]
    
    
    def get_queryset(self):
        employee: SalonEmployee = self.request.user.salon_user
        slots = []
        [slots.append(slot) for slot in employee.slots.all() if slot.date >= datetime.today().date()]
        if slots:
            return slots
        return AppointmentSlot.objects.none()

    
    
    
class AppViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self, **kwargs):
        appointment_slot_id = self.kwargs.get('appointment_slot_id')
        if appointment_slot_id:
            return Appointment.objects.filter(slot__id=appointment_slot_id, slot__employee=self.request.user.salon_user)
    
        return Appointment.objects.none()
    


@api_view(['PATCH'])
def approve_app(request, app_id):
    if request.method != 'PATCH':
        return Response({"error": "Invalid request method"})
    
    app = Appointment.objects.get(id=app_id)
    
    app.status = Appointment.StatusChoices.APPROVED
    
    app.save()
    
    
@api_view(['PATCH'])
def decline_app(request, app_id):
    if request.method != 'PATCH':
        return Response({"error": "Invalid request method"})
    
    app = Appointment.objects.get(id=app_id)
    
    app.status = Appointment.StatusChoices.DECLINED
    
    app.save()
    