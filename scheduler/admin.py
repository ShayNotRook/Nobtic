from django.contrib import admin
from .models import Salon, Service, AppointmentSlot, Appointment

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name', 'owner']
    
    
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'salon', 'provider', 'duration', 'price']
    
    


@admin.register(AppointmentSlot)
class AppointmentSlotAdmin(admin.ModelAdmin):
    list_display = ['id', 'salon', 'start_time', 'end_time', 'date', 'day', 'employee']
    list_filter = ['date']
    
    def day(self, obj: AppointmentSlot):
        return obj.day_fa
    
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["name", "app_start", "app_end", "slot__salon", "slot__day_of_week", "status"]
    list_filter = ["slot__date", "slot__salon", "slot__day_of_week"]
    
    
    def name(self, obj: Appointment):
        if obj.customer_name:
            return obj.customer_name
        else:
            return "Empty"