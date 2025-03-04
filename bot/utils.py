import os
from dotenv import load_dotenv

import random

import requests

from ext.melipayamak import Api

load_dotenv()
USERNAME = os.getenv('SMS_USER')
PASSWORD = os.getenv("SMS_PASS")
FROM_NUM = os.getenv("SMS_NUM")


def generate_verification_code(length=6):
    return ''.join(random.choices('0123456789', k=length))


def send_verify_code(code, phone_number):
    # SMS variables
    username, password = USERNAME, PASSWORD
    api = Api(username, password)
    sms = api.sms()
    to = phone_number
    _from = FROM_NUM
    message = f"کد تایید شما برای بات نوبت دهی: {code}"
    
    response = sms.send(to, _from, message)
    print(response)
    

def send_telegram_message(chat_id, message):
    TELEGRAM_BOT_TOKEN = os.getenv('TOKEN')
    TELEGRAM_MESSAGE_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(TELEGRAM_MESSAGE_API, data=data)
        response.raise_for_status()
        print(f"Message sent to {chat_id}")
        
    except requests.RequestException as e:
        print(f"Failed to send message: {e}")