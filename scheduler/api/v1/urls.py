from django.urls import path, include

from .api_views import ServiceViewSet, AppSlotViewSet, AppViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'services', ServiceViewSet, basename='service')
router.register(r'appointmentslots', AppSlotViewSet, basename='appointmentslot')

appointments_router = DefaultRouter()
appointments_router.register(r'appointments', AppViewSet, basename='appointment')

urlpatterns = [
    path('', include(router.urls)),
    path('appointmentslots/<int:appointment_slot_id>/', include(appointments_router.urls))
]
