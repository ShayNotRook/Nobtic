from django.apps import AppConfig
from django.core.management import call_command

import os
import threading
import asyncio

class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'
    
    
    
    def ready(self) -> None:
        # Starting bot in seperate thread to avoid blocking the server setup
        if os.environ.get("RUN_MAIN") == 'true':
            from django.core.management import call_command
            call_command("start_bot")