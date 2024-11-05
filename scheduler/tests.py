from django.test import TestCase

from .models import Salon, Service
# Create your tests here.

class TestSalon(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        test_case = Salon.objects.create()