# from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from scheduler.models import Service, Salon, AppointmentSlot, Appointment
from users.serializers import EmployeeSerializer


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'duration', 'price']
        # read_only_fields = ['id', 'salon', 'name']
        
        
class SalonSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Salon
        fields = ['id', 'name', 'employees', 'owner']
        
class AppointmentSerializer(serializers.ModelSerializer):
    # service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    # slot = serializers.PrimaryKeyRelatedField(queryset=AppointmentSlot.objects.all())
    service = serializers.StringRelatedField()
    class Meta:
        model = Appointment
        fields = ["id", "customer_name", "service", "app_start", "app_end", "status", "slot",
                  "receipt_txt", "receipt_img"]
        read_only_fields = ['id', 'status']
        
    def create(self, validated_data):
        service = validated_data.pop('service')
        slot = validated_data.pop('slot')

        appointment = Appointment.objects.create(service=service, slot=slot, **validated_data)
        return appointment

     
class AppSlotSerializer(serializers.ModelSerializer):
    appointments = AppointmentSerializer(many=True, read_only=True)
    
    def get_apps(self, obj):
        return obj.all_appointments
    
    class Meta:
        model = AppointmentSlot
        fields = ['id', 'date', 'day_of_week', 'appointments']
        read_only_fields = ['id', 'employee', 'date']
        

