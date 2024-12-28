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
    list_display = ['salon', 'start_time', 'end_time', 'date', 'day']
    
    def day(self, obj: AppointmentSlot):
        return obj.day_fa
    
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["name", "app_start", "app_end", "taken", "slot__salon", "slot__day_of_week"]
    list_filter = ["taken", "slot__date", "slot__salon", "slot__day_of_week"]
    
    
    def name(self, obj: Appointment):
        if obj.customer_name:
            return obj.customer_name
        else:
            return "Empty"