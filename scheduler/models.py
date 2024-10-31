from django.db import models


class Salon(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact = models.CharField(max_length=20)
    
    def __str__(self) -> str:
        return self.name
    
    
    
    
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
