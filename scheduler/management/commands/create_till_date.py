from django.core.management.base import BaseCommand
from scheduler.models import Salon


class Command(BaseCommand):
    help = "Create appointment slots till the given date"
    
    def add_arguments(self, parser):
        parser.add_argument('end_date', type=str, help="The end date in the format 'YYYY-MM-DD'")
        parser.add_argument("salon", type=str, help="The Salon name")
    
    def handle(self, *args, **options):
        end_date = options['end_date']
        salon = options['salon']
        salon = Salon.objects.get(name=salon)
        
        
        salon.create_slots_until_date(end_date)
        self.stdout.write(self.style.SUCCESS("Appointment slots created successfully"))