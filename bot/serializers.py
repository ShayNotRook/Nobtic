from rest_framework import serializers

from scheduler.models import Service, Salon
from users.models import SalonEmployee

class ServiceSerializerBot(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'duration', 'price']


class EmployeesSerializerBot(serializers.ModelSerializer):
    services = ServiceSerializerBot(many=True)
    
    class Meta:
        model = SalonEmployee
        fields = ['id', 'name', 'services', 'card_num']

class SalonSerializerBot(serializers.ModelSerializer):
    employees = EmployeesSerializerBot(many=True)
    
    class Meta:
        model = Salon
        fields = ['id', 'name', 'employees']
        
        
class AvailableSlotSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateField()
    time_ranges = serializers.ListField(child=serializers.CharField())