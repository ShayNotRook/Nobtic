from django.contrib import admin
from .models import Salon, Service

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
    
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'salon')