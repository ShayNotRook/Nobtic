from rest_framework import serializers

from .models import SalonEmployee

from scheduler.models import Service

class EmployeeSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)
    
    class Meta:
        model = SalonEmployee
        fields = ['name', 'services']
        
        