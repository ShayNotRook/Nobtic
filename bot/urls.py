from django.urls import path

from .views import (GetSalonView, GetAvailableSlots, update_app,
                    send_verification_sms, verify_code, create_unpaid_app)

urlpatterns = [
    # <---Initial endpoints to fetch salon, employee and service data--->
    path('api/salons/<slug:slug>/', GetSalonView.as_view(), name='salon-view'),
    path('api/available-slots/', GetAvailableSlots.as_view(), name='available-slots'),
    
    # <---Phone num verifications--->
    path('api/send_verification_code/', send_verification_sms, name='send_verify_code'),
    path('api/verify_code/', verify_code, name='verify_code'),
    
    # <---Appointment controllers--->
    path('api/app/create/', create_unpaid_app, name='create_app'),
    path('api/app/update/<int:app_id>', update_app, name='update_appointment'),
]