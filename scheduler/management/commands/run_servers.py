from django.core.management.base import BaseCommand

import os
import sys
import asyncio
from multiprocessing import Process

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from scheduler.bot.main import main as start_bot

def start_django():
    os.system("python manage.py runserver")
    
def run_bot():
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(start_bot())
    start_bot()

class Command(BaseCommand):
    help = "Start both django server and Telegram bot"
    
    
    def handle(self, *args, **options):
        django_process = Process(target=start_django)
        bot_process = Process(target=start_bot)
        
        try:
            django_process.start()
            bot_process.start()
            
            django_process.join()
            bot_process.join()
            
            self.stdout.write(self.style.SUCCESS("Processes started successfully."))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR("Error: {e}"))
            
        finally:
            django_process.terminate()
            bot_process.terminate()
            django_process.join()
            bot_process.join()
            self.stdout.write(self.style.SUCCESS("Processes terminated successfully."))