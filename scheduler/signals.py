from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import AppointmentSlot

@receiver(post_save, sender=AppointmentSlot)
def generate_apps(sender, instance, created, **kwargs):
    """
    Signal to generate appointments when an AppointmentSlot is created.
    """
    if created:
        service_duration = 60
        instance.create_appointments(service_duration)
        
        
        
@receiver(post_save, sender=AppointmentSlot)
def update_active_status(sender, instance: AppointmentSlot, **kwargs):
    instance.check_and_update_active_status()

