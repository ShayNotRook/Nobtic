from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    

card_number_validator = RegexValidator(
    regex=r'^\d{16}$',
    message="Card number must be exactly 16 digits."
)

class SalonEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='salon_user', null=True)
    salon = models.ForeignKey('scheduler.Salon', on_delete=models.CASCADE, related_name='employees')
    name = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    card_num = models.CharField(max_length=19, unique=True, null=True, validators=[card_number_validator])
    
    def __str__(self):
        return f"{self.name} - {self.salon.name}"
    
    
    def format_card_num(self):
        cleaned_num = self.card_num.replace(" ", "")
        return " ".join([cleaned_num[i:i+4] for i in range(0, len(cleaned_num), 4)])
    
    
    def save(self, *args, **kwargs):
        self.card_num = self.format_card_num()
        super().save(*args, **kwargs)
        
        
    
    def get_services(self):
        services_name = []
        
        for service in self.services.all():
            services_name.append(service.name)
            
        return services_name
    
    def get_slots(self):
        return self.slots.all()
    
    
    def get_available_slots_by_service(self, service_duration):
        slots = self.get_slots()
        available_slots = []
        
        for slot in slots:
            if (available_ranges := slot.service_fits(service_duration)):
                available_slots.append((slot.id, slot.date.strftime("%Y-%m-%d"), available_ranges))
        
        
        return available_slots