from typing import List
from datetime import time

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()
BOT_USERNAME = "salon_scheduler_bot"



class Salon(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True)
    address = models.TextField()
    contact = models.CharField(max_length=20)
    owner = models.OneToOneField(User, on_delete=models.PROTECT, null=True, related_name='owner')
    telegram_link = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        self.telegram_link = self.generate_bot_link()
        
        super().save(*args, **kwargs)
    
    def generate_bot_link(self):
        bot_username = BOT_USERNAME
        return f"https://t.me/{bot_username}?start={self.slug}"
    
    def create_slots_until_date(self, end_date: str, emp_id) -> None:
        """
        Creates appointment slots until the given end_date.

        Parameters:
        end_date (str): The end date in the format "YYYY-MM-DD".
        """
        from datetime import timedelta, datetime
        from persiantools.jdatetime import JalaliDate
                
        end_date = JalaliDate(*map(int, end_date.split('-')), locale="fa").to_gregorian()
        current_date = JalaliDate.today().to_gregorian()
        days_till_end_date: timedelta = end_date - current_date
        
        slots_to_create: List['AppointmentSlot'] = [] # Stores AppointmentSlot objects to be bulk created
    
            
        for day in range(days_till_end_date.days + 1):
            single_date = current_date + timedelta(days=day)
            if not AppointmentSlot.objects.filter(salon=self, date=single_date).exists():
                slot = AppointmentSlot(salon=self, date=single_date)
                slot.save()
                slots_to_create.append(slot)
        
        
        if slots_to_create:
            created_slots = AppointmentSlot.objects.bulk_create(slots_to_create, ignore_conflicts=True)
            print(f"Created {len(created_slots)} appointment slots.")
        
        else:
            print("No new appointment slots needed.")
    
    class Meta:
        verbose_name = 'Salon Model'    
    
    
class Service(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    price = models.IntegerField(help_text="Enter the price in Toman (e.g., 50000 for 50,000 Toman)", default=0)
    provider = models.ForeignKey('users.SalonEmployee', on_delete=models.PROTECT, related_name='services', null=True)
    

    def __str__(self) -> str:
        return self.name
    
    def asave(self, force_insert = ..., force_update = ..., using = ..., update_fields = ...):
        return super().asave(force_insert, force_update, using, update_fields)
    
    
class AppointmentSlot(models.Model):
    
    class DayOfWeek(models.TextChoices):
        SATURDAY = 'Saturday'
        SUNDAY = 'Sunday'
        MONDAY = 'Monday'
        TUESDAY = 'Tuesday'
        WEDNESDAY = 'Wednesday'
        THURSDAY = 'Thursday'
        FRIDAY = 'Friday'
        
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, null=True)
    employee = models.ForeignKey('users.SalonEmployee', null=True, on_delete=models.PROTECT, related_name='slots')
    date = models.DateField(db_index=True)
    start_time = models.TimeField(default=time(8, 0))
    end_time = models.TimeField(default=time(20, 0))
    day_of_week = models.CharField(max_length=12, choices=DayOfWeek.choices, null=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["salon", "date", "start_time", "end_time"],
                name="unique_slot_per_salon"
            )
        ]
    
    
    # Class methods
    def __str__(self) -> str:
        return f"{self.date}"
    
    def save(self, *args, **kwargs):
        self.day_of_week = self.date.strftime('%A')
        super().save(*args, **kwargs)
    
    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time")
        
    def check_and_update_active_status(self):
        from datetime import datetime
        
        now = datetime.now().time()
        if self.end_time < now:
            self.active = False
            self.save()
    
    
    # Properties
    @property
    def day_fa(self):
        farsi_days = {
            'Saturday': 'شنبه',
            'Sunday': 'یکشنبه',
            'Monday': 'دوشنبه',
            'Tuesday': 'سه شنبه',
            'Wednesday': 'چهارشنبه',
            'Thursday': 'پنجشنبه',
            'Friday': 'جمعه'
        }
        return farsi_days.get(self.day_of_week)
    
    @property
    def day_display_custom(self):
        return f"{self.day_of_week} / {self.get_day_fa()}"
        
    
    @property
    def all_appointments(self) -> List["Appointment"]:
        return self.appointments.all()
    

            
    # Util functions
    @staticmethod
    def create_slots_until_date( end_date: str, employee) -> None:
        """
        Creates appointment slots until the given end_date.

        Parameters:
        end_date (str): The end date in the format "YYYY-MM-DD".
        """
        from datetime import timedelta
        from persiantools.jdatetime import JalaliDate
                
        end_date = JalaliDate(*map(int, end_date.split('-')), locale="fa").to_gregorian()
        current_date = JalaliDate.today().to_gregorian()
        days_till_end_date: timedelta = end_date - current_date
        
        slots_to_create: List['AppointmentSlot'] = [] # Stores AppointmentSlot objects to be bulk created
    
            
        for day in range(days_till_end_date.days + 1):
            single_date = current_date + timedelta(days=day)
            if not AppointmentSlot.objects.filter(employee=employee, date=single_date).exists():
                slot = AppointmentSlot(employee=employee, salon = employee.salon, date=single_date,
                                        start_time=employee.preferred_start, end_time=employee.preferred_end)
                slot.save()
                slots_to_create.append(slot)
        
        if slots_to_create:
            created_slots = AppointmentSlot.objects.bulk_create(slots_to_create, ignore_conflicts=True)
            print(f"Created {len(created_slots)} appointment slots.")
        
        else:
            print("No new appointment slots needed.")
    
    
    
    def get_available_ranges(self):
        """
            This method returns the unappointed time ranges available within a slot
            
            Returns:
                List[Tuple[datetime.time, datetime.time]] - Available time ranges without any appointments
        """
        ranges = []
        apps = self.all_appointments.order_by('app_start')
        
        # Time formatter(Removes the seconds slice from time object)
        def format_time(t):
            return t.strftime("%H:%M")
        
        
        if not apps.exists():
            ranges.append(f"{format_time(self.start_time)} - {format_time(self.end_time)}")
        else:
            if self.start_time < apps[0].app_start:
                ranges.append(f"{format_time(self.start_time)} - {format_time(apps[0].app_start)}")
                
            for index in range(1, len(apps)):
                if apps[index - 1].app_end < apps[index].app_start:
                    ranges.append(f"{format_time(apps[index - 1].app_end)} - {format_time(apps[index].app_start)}")
            
            last_app = apps.order_by('-id').first()
            if last_app.app_end < self.end_time:
                ranges.append(f"{format_time(last_app.app_end)} - {format_time(self.end_time)}")
                
        return ranges
    
    
    def service_fits(self, service_duration_minutes):
        from datetime import datetime, timedelta
        """
            This method checks if the given service can fit within any available time range
            within a slot.
            Return a list of available start times.
            
            Parameters:
                service_duration_minues: int - The duration of the service in minutes.
                
            Returns:
                List[datetime.time] - Available start times for the service
        """
        
        available_start_times = []
        time_ranges = self.get_available_ranges()
        
        
        for time_range in time_ranges:
            start, end = [datetime.strptime(t.strip(), "%H:%M").time() for t in time_range.split(' - ')]
            # duration = timedelta(minutes=service_duration_minutes)
            
                   
            end_datetime = datetime.combine(self.date, end)
            duration_timedelta = timedelta(minutes=service_duration_minutes)
            max_start_time = (end_datetime - duration_timedelta).time()
            
            
            if max_start_time > start:
                available_start_times.append(f"{start.strftime('%H:%M')} - {max_start_time.strftime('%H:%M')}")
                
            elif max_start_time == start:
                available_start_times.append(start.strftime("%H:%M"))
                
                
        return available_start_times
    

def appointment_images_upload_to(instance: 'Appointment', filename):
    return f"backend/app_receipts/{instance.slot.employee.username}/receipt_imgs/{filename}"
    
class Appointment(models.Model):
    
    class StatusChoices(models.TextChoices):
        DECLINED = 'رد شده'
        NOT_PAID = 'پرداخت نشده'
        PENDING = 'در انتظار تایید'
        APPROVED = 'تایید شده'
        
    customer_name = models.CharField(max_length=100, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    slot = models.ForeignKey(AppointmentSlot, on_delete=models.CASCADE, related_name="appointments", null=True)
    app_start = models.TimeField(null=True)
    app_end = models.TimeField(null=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.NOT_PAID)
    telegram_chat_id = models.BigIntegerField(null=True)
    receipt_txt = models.TextField(null=True, blank=True)
    receipt_img = models.ImageField(upload_to=appointment_images_upload_to, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.customer_name if self.customer_name else ''} on \
                 {self.slot.date} at {self.app_start} to {self.app_end}"
    
    def clean(self):
        if not self.customer_name:
            raise ValueError("Appointment object should include the customer's name")
        
        if self.app_start >= self.app_end:
            raise ValidationError("Start time must be before end time")
        
    
    def get_receipt_url(self):
        """
            Returns the URL for the receipt image, if available.
        """
        if self.receipt_img:
            return self.receipt_img.url
        return None