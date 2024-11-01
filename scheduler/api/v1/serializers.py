from rest_framework.serializers import ModelSerializer

from scheduler.models import Service

class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'salon', 'name', 'duration_time']
        read_only_fields = ['id', 'salon']