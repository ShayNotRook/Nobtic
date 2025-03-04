from django.contrib import admin

from .models import User, SalonEmployee


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_superuser']


@admin.register(SalonEmployee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["id", 'salon__name', 'name', 'services', 'card_num']
    
    
    def services(self, obj):
        return obj.get_services()