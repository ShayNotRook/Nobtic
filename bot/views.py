from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view

from datetime import datetime, timedelta

from scheduler.models import AppointmentSlot, Appointment, Salon, Service
from scheduler.api.v1.serializers import AppointmentSerializer
from users.models import SalonEmployee

from .models import VerificationCode
from .serializers import SalonSerializerBot, AvailableSlotSerializer
from .utils import generate_verification_code, send_verify_code


class GetSalonView(generics.RetrieveAPIView):
    queryset = Salon.objects.all().prefetch_related('employees__services')
    serializer_class = SalonSerializerBot
    lookup_field = 'slug'
    

class GetAvailableSlots(APIView):
    def get(self, request, format=None):
        employee_id = request.query_params.get('employee_id')
        service_id = request.query_params.get('service_id')
        
        if not employee_id or not service_id:
            return Response(
                {"error": "employee_id and service_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        employee = get_object_or_404(SalonEmployee, id=employee_id)
        service = get_object_or_404(Service, id=service_id)
        
        available_slots = employee.get_available_slots_by_service(service.duration)
        
        
        slots_data = []
        for slot_id, slot_date, slot_ranges in available_slots:
            slots_data.append({
                "id": slot_id,
                "date": slot_date,
                "time_ranges": slot_ranges
            })
            
        serializer = AvailableSlotSerializer(slots_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


        
# Code Verification Views
@api_view(['GET'])
def send_verification_sms(request):
    phone = request.GET.get('phone')
    if not phone:
        return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    code = generate_verification_code()
    
    VerificationCode.objects.create(phone_number=phone, code=code)
    
    send_verify_code(code, phone)
    
    return Response({"valid": True,"message": "Verification code sent (test code)"})


@api_view(['GET'])
def verify_code(request):
    phone = request.GET.get("phone")
    code = request.GET.get('code')
    
    if not phone or not code:
        return Response({"error": "Phone number and code are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        verification_record = VerificationCode.objects.filter(phone_number=phone, code=code).latest('created_at')
    except VerificationCode.DoesNotExist:
        return Response({"valid": False, 'error': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)
    
    expiration_minute = 5
    if verification_record.created_at + timedelta(minutes=expiration_minute) < datetime.now(verification_record.created_at.tzinfo):
        return Response({'valid': False, 'error': 'Verification code expired.'}, status=status.HTTP_400_BAD_REQUEST)
    
    verification_record.used = True
    return Response({'valid': True, 'message': 'Verification successfull.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_unpaid_app(request):
    if request.method != "POST":
        return Response({"error": "Invalid request method"})    
        
    data = request.data
        
    customer_name = data.get("customer_name")
    slot_id = data.get("slot")
    service_id = data.get("service")
    app_start_str = data.get("app_start")
    chat_id = data.get("chat_id")
    receipt_txt = data.get("receipt_txt", "")
    
    if not all([customer_name, slot_id, service_id, app_start_str]):
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        slot = AppointmentSlot.objects.get(id=slot_id)
        service = Service.objects.get(id=service_id)
        
        dummy_date = datetime.now()
        
        app_start_dt = datetime.strptime(f"{dummy_date.strftime('%Y-%m-%d')} {app_start_str}", "%Y-%m-%d %H:%M")
        app_end_dt = app_start_dt + timedelta(minutes=service.duration)
        
        app_start = app_start_dt.time()
        app_end = app_end_dt.time()
        
        
        appointment = Appointment.objects.create(
            customer_name = customer_name,
            service = service,
            slot = slot,
            app_start = app_start,
            app_end = app_end,
            status = Appointment.StatusChoices.NOT_PAID,
            telegram_chat_id = chat_id
        )
        
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except AppointmentSlot.DoesNotExist:
        return Response({"error": "Invalid slot id."}, status=status.HTTP_400_BAD_REQUEST)
    except Service.DoesNotExist:
        return Response({"error": "Invalid service id."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
    
    

@api_view(['PATCH'])
def update_app(request, app_id):
    if request.method != 'PATCH':
        return Response({"error": "Invalid request method"})
    
    try:
        appointment = Appointment.objects.get(id=app_id)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found!"})
    
    receipt_txt = request.data.get("receipt_txt")
    if receipt_txt is not None:
        appointment.receipt_txt = receipt_txt
    
    if "receipt_img" in request.FILES:
        receipt_img = request.FILES['receipt_img']
        appointment.receipt_img = receipt_img
            
    new_status = request.data.get('status')
    
    valid_statuses = [choice[0] for choice in Appointment.StatusChoices.choices]
    
    if new_status not in valid_statuses:
        return Response(
            {"message": "Invalid status. Allowed values: " + ", ".join(valid_statuses)},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    appointment.status = new_status
    appointment.save()
    
    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data, status=status.HTTP_200_OK)