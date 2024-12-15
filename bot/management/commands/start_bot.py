import asyncio
from typing import Any
import os
import threading

from django.core.management.base import BaseCommand

from bot.main import main as bot_main

LOCK_FILE = 'bot.lock'

class Command(BaseCommand):
    help = "Starts the Telegram bot"
    
    def handle(self, *args: Any, **kwargs: Any) -> None:
        self.stdout.write(self.style.SUCCESS("Starting the telegram bot..."))

        if os.path.exists(LOCK_FILE):
            self.stdout.write(self.style.ERROR("Bot is already running"))
        
        open(LOCK_FILE, 'w').close()
        
        try:
            bot_thread = threading.Thread(target=bot_main, daemon=True)
            bot_thread.start()
            self.stdout.write("Bot started in a seperate thread.")
            # asyncio.run(main())
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error starting bot: {e}"))()
            
        finally:
            # Remove lock file
            if os.path.exists(LOCK_FILE):
                os.remove(LOCK_FILE)

            
            