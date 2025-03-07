from django.core.management.base import BaseCommand
from scheduler.models import AppointmentSlot
from users.models import SalonEmployee

class Command(BaseCommand):
    help = "Create appointment slots till the given date"
    
    def add_arguments(self, parser):
        parser.add_argument('end_date', type=str, help="The end date in the format 'YYYY-MM-DD'")
        parser.add_argument("employee_id", type=str, help="The Salon name")
    
    def handle(self, *args, **options):
        end_date = options['end_date']
        employee_id = options['employee_id']
        employee = SalonEmployee.objects.get(id=employee_id)
        
        
        AppointmentSlot.create_slots_until_date(end_date, employee)
        self.stdout.write(self.style.SUCCESS("Appointment slots created successfully"))