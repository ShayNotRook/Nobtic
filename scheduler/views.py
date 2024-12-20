from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import AppointmentSlot, Salon


@login_required
def all_apps(request):
    user = request.user
    print(user)
    today = datetime.now().date()
    app_slot = AppointmentSlot.objects.filter(salon__owner=user, date=today)
    print(app_slot)
    apps = []
    for slot in app_slot:
        apps.extend(slot.all_appointments)
    print("Debug")
    return render(request, 'appointments.html', {'appointments': apps})