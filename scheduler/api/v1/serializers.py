from rest_framework.serializers import ModelSerializer

from scheduler.models import Service, Salon

class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'salon', 'name', 'duration_time']
        read_only_fields = ['id', 'salon']
        
        
class SalonSerializer(ModelSerializer):
    class Meta:
        model = Salon
        fields = '__all__'