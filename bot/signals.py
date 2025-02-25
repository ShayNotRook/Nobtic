from django.db.models.signals import post_save
from django.dispatch import receiver

from scheduler.models import Appointment

from .utils import send_telegram_message

@receiver(post_save, sender=Appointment)
def appoint_status_change(sender, instance: Appointment, created, **kwargs):
    if not created and instance.status == Appointment.StatusChoices.APPROVED:
        chat_id = instance.telegram_chat_id
        if chat_id:
            message = "🎉 نوبت شما تایید شد!"
            send_telegram_message(chat_id=chat_id, message=message)