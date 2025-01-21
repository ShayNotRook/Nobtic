import aiohttp

API = "http://localhost:8000/schedule/api/v1"


async def get_apps_by_salon_id(id: int, session_id):
    headers = {
        "Session-ID": session_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API}/appointmentslots?salon_id={id}", headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return []
        
        

async def get_apppointments_by_slot_id(slot_id: int, session_id):
    headers = {
        "Session-ID": session_id
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API}/appointmentslots/{slot_id}/appointments") as response:
            if response.status == 200:
                return await response.json()
            return []
        
  
  
  
async def book_appointment(appointment_id: int, name: str, session_id):
    headers = {
        "Session-ID": session_id,
        'Content-Type': "application/json"
    }
    
    data = {
        "appointment_id": appointment_id,
        "name": name
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API}/book_app/", headers=headers, json=data) as response:
            return await response.json()
        