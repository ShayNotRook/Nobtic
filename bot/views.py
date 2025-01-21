from django.shortcuts import render, get_object_or_404

from rest_framework.generics import ListAPIView

from scheduler.models import AppointmentSlot, Appointment, Salon
from scheduler.api.v1.serializers import AppointmentSerializer, AppSlotSerializer

from datetime import datetime

class ListAppSlots(ListAPIView):
    serializer_class = AppSlotSerializer
    
    def get_queryset(self):
        salon = get_object_or_404(Salon, id=self.kwargs.get('salon_id'))
        return AppointmentSlot.objects.filter(salon=salon, active=True)
    
    
class ListAppsBySlot(ListAPIView):
    serializer_class = AppointmentSerializer
    
    def get_queryset(self):
        slot_id = self.kwargs.get("slot_id")
        slot = get_object_or_404(AppointmentSlot, id=slot_id)
        return Appointment.objects.filter(slot=slot)    

# Bot APIs
# def get_app_slots(request, salon_id):
#     if request.method == "GET":
#         salon = get_object_or_404(Salon, id=salon_id)
#         app_slots = AppointmentSlot.objects.filter(salon=salon, active=True)
#         serializer = AppointmentSerializer(app_slots, many=True)
#         return

# def get_apps_by_slot(request, slot_id):
#     slot = get_object_or_404(AppointmentSlot, id=slot_id)
#     return Appointment.objects.filter(slot=slot)
