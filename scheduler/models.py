from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

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
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")
          
    
    class Meta:
        verbose_name = 'Available time'
    
class Service(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    duration_time = models.PositiveIntegerField()
    
    def __str__(self) -> str:
        return f"{self.name} - {self.salon.name}"
    
    

class Appointment(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    
    def __str__(self) -> str:
        return f"{self.customer_name} - {self.service.name} on {self.date} at {self.time}"
