from typing import Any
from django.core.management.base import BaseCommand
from scheduler.bot import main


class Command(BaseCommand):
    help = "Starts the Telegram bot"
    
    def handle(self, *args: Any, **kwargs: Any) -> None:
        main()