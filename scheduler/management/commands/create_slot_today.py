from django.core.management.base import BaseCommand
from django.utils import timezone
from scheduler.models import AppointmentSlot, Salon

class Command(BaseCommand):
    help = "Create appointment slots for the current day"
    
    def handle(self, *args, **options):
        today = timezone.now().date()
        salons = Salon.objects.all()
        for salon in salons:
            if not AppointmentSlot.objects.filter(salon=salon, date=today).exists():
                AppointmentSlot.objects.create(salon=salon, date=today)
                self.stdout.write(self.style.SUCCESS("Appointment slot created successfully"))
            else:
                self.stdout.write(self.style.WARNING("Appointment slot already exists for today"))