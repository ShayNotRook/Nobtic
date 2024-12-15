from typing import Iterable
from datetime import time

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator



User = settings.AUTH_USER_MODEL

class Salon(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True)
    address = models.TextField()
    contact = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Salon Model'    


class SalonAvailableTimes(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = models.CharField(max_length=12, choices=[
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday')
    ]) 
    
    def __str__(self) -> str:
        return f"{self.salon}"
    
    
    def clean(self) -> None:
        if self.start_time > self.end_time:
            raise ValidationError("Start time must be before end time")
        if self.start_time < time(0, 0) or self.end_time > time(23, 59):
            raise ValidationError("Time must be within a valid 24-hour range.")
          
    
    class Meta:
        verbose_name = 'Available time'
    
class Service(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    duration_time = models.PositiveIntegerField()
    
    def __str__(self) -> str:
        return f"{self.name} - {self.salon.name}"
    
    
    
class AppointmentSlot(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["salon", "date", "start_time", "end_time"],
                name="unique_slot_per_salon"
            )
        ]
    
    def __str__(self) -> str:
        return f"{self.salon.name} => {self.date}"
    
    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time")
        
    
    
    

class Appointment(models.Model):
    customer_name = models.CharField(max_length=100, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    slot = models.ForeignKey(AppointmentSlot, on_delete=models.CASCADE, related_name="app_slot", null=True)
    taken = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.customer_name} - {self.service.name} on {self.slot.date} at {self.slot.start_time}"
    
    
    class Meta:
        unique_together = ["app_slot.id", "app_slot.start_time", "app_slot.end_time"]
