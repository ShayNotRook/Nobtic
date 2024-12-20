from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from datetime import datetime
from .models import AppointmentSlot, Salon


_user = get_user_model()


@login_required
def all_apps(request: HttpRequest):
    # print(request.__dir__())
    user = _user.objects.get(username=request.user.username)
    print(user)
    today = datetime.now().date()
    app_slot = AppointmentSlot.objects.get(salon__owner=user)
    salon_name = app_slot.salon.name
    print(app_slot)
    apps = app_slot.all_appointments
    
    # print(print(apps))
    return render(request, 'appointments.html', {'appointments': apps, 'user': user, 'name': salon_name})