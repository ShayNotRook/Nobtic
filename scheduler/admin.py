from django.contrib import admin
from .models import Salon, Service, SalonAvailableTimes, AppointmentSlot, Appointment

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name', 'owner']
    
    
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'salon')
    
    
# @admin.register(SalonAvailableTimes)
# class TimesAdmin(admin.ModelAdmin):
#     list_display = ['salon', 'start_time', 'end_time']
    

@admin.register(AppointmentSlot)
class AppointmentSlotAdmin(admin.ModelAdmin):
    list_display = ['salon', 'start_time', 'end_time', 'date']
    
admin.site.register(Appointment)