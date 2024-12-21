from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from typing import List
from datetime import datetime
from .models import AppointmentSlot, Appointment


_user = get_user_model()


@login_required
def all_apps(request: HttpRequest):
    user = _user.objects.get(username=request.user.username)
    salon_name = user.salon.name
    today = datetime.now().date()
    apps = []
    try:
        app_slot = AppointmentSlot.objects.get(salon__owner=user, date__gte=today)
        apps = app_slot.all_appointments.all()
    except AppointmentSlot.DoesNotExist:
        apps = None
    # print(print(apps))
    return render(request, 'appointments.html', {'appointments': apps, 'user': user, 'name': salon_name})