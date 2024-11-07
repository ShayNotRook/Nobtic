import asyncio
from typing import Any

from django.core.management.base import BaseCommand

from bot.main import main

class Command(BaseCommand):
    help = "Starts the Telegram bot"
    
    def handle(self, *args: Any, **kwargs: Any) -> None:
        self.stdout.write(self.style.SUCCESS("Starting the telegram bot..."))

        try:
            # Check if an event loop is already running
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                # No event loop is running: create a new one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            
            loop.create_task(main())
            
            loop.run_until_complete() 
            
                           
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error starting bot: {e}"))
            
            