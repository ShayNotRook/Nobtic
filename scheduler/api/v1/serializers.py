# from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from scheduler.models import Service, Salon, AppointmentSlot, Appointment

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'salon', 'name', 'duration_time']
        read_only_fields = ['id', 'salon', 'name']
        
        
class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = '__all__'
        
class AppointmentSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    
    class Meta:
        model = Appointment
        fields = ["id", "customer_name", "service", "app_start", "app_end", "taken", "slot"]

     
class AppSlotSerializer(serializers.ModelSerializer):
    
    appointments = AppointmentSerializer(many=True, read_only=True)
    
    def get_apps(self, obj):
        return obj.all_appointments
    
    class Meta:
        model = AppointmentSlot
        fields = '__all__'
        read_only_fields = ['id', 'salon']
        

