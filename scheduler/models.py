from typing import List
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
        
    def create_appointments(self, service_duration: int):
        from datetime import datetime, timedelta
        
        start = datetime.combine(self.date, self.start_time)
        end = datetime.combine(self.date, self.end_time)
        current = start
        
        while current + timedelta(minutes=service_duration) <= end:
            Appointment.objects.create(
                slot=self,
                app_start=current.time(),
                app_end=(current + timedelta(minutes=service_duration)).time(),
                taken=False
            )
            current += timedelta(minutes=service_duration)
    
    @property
    def all_appointments(self) -> List["Appointment"]:
        return self.appointments.all()
    

class Appointment(models.Model):
    customer_name = models.CharField(max_length=100, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    slot = models.ForeignKey(AppointmentSlot, on_delete=models.CASCADE, related_name="appointments", null=True)
    taken = models.BooleanField(default=False)
    app_start = models.TimeField(null=True)
    app_end = models.TimeField(null=True)
    
    def __str__(self) -> str:
        return f"{self.customer_name if self.customer_name else ''} on \
                 {self.slot.date} at {self.app_start} to {self.app_end} -> {'Taken' if self.taken else 'Available'}"
    
    
    @staticmethod
    def find_available_slots(slot: AppointmentSlot, duration: int) -> List["Appointment"] :
        """
        Find smaller available time slots within the given AppointmentSlot.
        """
        available = []
        appointments = slot.appointments.filter(taken=False).order_by("app_start")
        for appointment in appointments:
            # Check if the duration fits in the current appointment
            if (appointment.app_end.hour * 60 + appointment.app_end.minute) - (
                appointment.app_start.hour * 60 + appointment.app_start.minute
            ) >= duration:
                available.append(appointment)
        return available
    
    
    
    @staticmethod
    def book_app(id: int, name: str) -> None:
        try:
            app = Appointment.objects.get(id=id)
            if app.taken:
                raise ValidationError("This appointment is already taken.")
            app.customer_name = name
            app.taken = True
            app.save()
        except Appointment.DoesNotExist:
            raise ValidationError("Appointment with the given ID does not exist.")
    
    
    
