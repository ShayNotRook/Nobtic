import random


def generate_verification_code(length=6):
    return ''.join(random.choices('0123456789', k=length))


def send_test_sms(phone_number, message):
    print(f"Sending SMS to {phone_number}: {message}")