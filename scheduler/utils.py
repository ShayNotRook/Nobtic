from .models import AppointmentSlot
from datetime import timedelta, time

# This class represents a time range
class TimeInterval:
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end
        
    def overlaps(self, other: 'TimeInterval') -> bool:
        return self.start < other.end and self.end > other.start
    
    def contains(self, other: 'TimeInterval') -> bool:
        return self.start <= other.start and self.end >= other.end
    
    
"""
    Represent the entire slot
    Fetch all "Appointment" records 
    for the slot and convert them into
    "TimeInterval" objects
"""
def get_all_intervals(slot: AppointmentSlot):
    booked_appointments = slot.appointments.all().order_by('start_time')
    available_appointments = []
    
    previous_end = slot.start_time
    
    for app in booked_appointments:
        if previous_end < app.start_time:
            pass