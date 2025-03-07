import aiohttp

# Data classes made to hold the data fetched from api
from bot.dataclasses import Salon, Employee, Service
from .util_funcs import create_slot_by_date

API = "https://nobtic.ir/backend/bot/api"


async def fetch_salon_data(slug: str) -> Salon:
    async with aiohttp.ClientSession() as session:
        response = await session.get(f"{API}/salons/{slug}/")
        response.raise_for_status()
        response = await response.json()
        
        return Salon(
            id=response.get('id'),
            name=response.get('name'),
            employees=[
                Employee(
                    id=emp['id'],
                    name=emp['name'],
                    services=[Service(**service) for service in emp['services']],
                    card_num=emp['card_num']
                ) for emp in response['employees']
            ]
        )    
    

async def fetch_available_slots(employee_id, service_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{API}/available-slots/?employee_id={employee_id}&service_id={service_id}"
            ) as response:
            response.raise_for_status()
            response = await response.json()
        
            slots = []
        
            for slot in response:
                slots.append(create_slot_by_date(slot=slot))
        
            return slots
        
        
async def send_verify_code(phone_num: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{API}/send_verification_code/?phone={phone_num}"
            ) as response:
            response.raise_for_status()
            data = await response.json()
            return data
        
        
async def verify_code(phone_num: str, code: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{API}/verify_code/?phone={phone_num}&code={code}"
            ) as response:
            response.raise_for_status()
            data = await response.json()
            print(data)
            return data
        

async def create_appointment(payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{API}/app/create/",
                data=payload,
            ) as response:
            response.raise_for_status()
            data = await response.json()
            return data
        

async def update_appointment(app_id: int, payload):
    async with aiohttp.ClientSession() as session:
        async with session.patch(
                f"{API}/app/update/{app_id}",
                data=payload
            ) as response:
            response.raise_for_status()
            data = await response.json()
            return data