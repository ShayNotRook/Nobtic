from dataclasses import dataclass
from typing import List

from datetime import date


@dataclass
class Service:
    id: int
    name: str
    duration: int # Minutes
    price: int
    
    
@dataclass
class Employee:
    id: int
    name: str
    services: List[Service]
    card_num: str
    
    
@dataclass
class Salon:
    id: int
    name: str
    employees: List[Employee]
    
    
@dataclass(slots=True)
class Slot:
    id: int
    date: date
    time_ranges: List[str]