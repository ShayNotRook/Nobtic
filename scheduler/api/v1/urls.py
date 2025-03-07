from django.urls import path, include

from .api_views import ServiceViewSet, AppSlotViewSet, AppViewSet, approve_app

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'services', ServiceViewSet, basename='service')
router.register(r'appointmentslots', AppSlotViewSet, basename='appointmentslot')

appointments_router = DefaultRouter()
appointments_router.register(r'appointments', AppViewSet, basename='appointment')

urlpatterns = [
    path('', include(router.urls)),
    # path('book_app/', book_appointment, name='book_app'),
    path('appointmentslots/<int:appointment_slot_id>/', include(appointments_router.urls)),
    path('app/approve/<int:app_id>', approve_app, name='approve-appointment'),
]
