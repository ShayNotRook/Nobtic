from django.db import models

# Create your models here.

class VerificationCode(models.Model):
    phone_number = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.phone_number}: {self.code}"
    

class AppointmentLog(models.Model):
    customer_name = models.CharField(max_length=40)
    salon = models.ForeignKey('scheduler.Salon', on_delete=models.PROTECT, related_name='logs')
    slot = models.ForeignKey('scheduler.AppointmentSlot', on_delete=models.PROTECT, related_name='app_logs')