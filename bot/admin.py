from django.contrib import admin
from .models import VerificationCode

# Register your models here.

@admin.register(VerificationCode)
class CodeAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'code']