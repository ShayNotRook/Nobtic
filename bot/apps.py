from django.apps import AppConfig
from django.core.management import call_command

import threading
import asyncio

class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'
    
    
    
    def ready(self) -> None:
        # Starting bot in seperate thread to avoid blocking the server setup
        threading.Thread(target=self.start_bot_command).start()
    
        
    def start_bot_command(self) -> None:
        try:
            call_command("start_bot")
        except Exception as e:
            print(f"Error starting the bot: {e}")