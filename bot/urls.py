from django.urls import path

from .views import ListAppSlots, ListAppsBySlot

urlpatterns = [
    path('salon/<int:salon_id>/slots', ListAppSlots.as_view(), name='app_slots'),
    path('slots/<int:slot_id>/', ListAppsBySlot.as_view(), name='apps_by_slot')
]