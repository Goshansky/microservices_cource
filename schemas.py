from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from enum import Enum
from typing import List


class ClientInput(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    email: EmailStr
    phone_number: constr(pattern=r'^\+?1?\d{9,15}$')
    password: str
    timestamp: datetime


class Client(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    email: EmailStr
    phone_number: constr(pattern=r'^\+?1?\d{9,15}$')
    password: str
    timestamp: datetime

    class Config:
        from_attributes = True


class EmailUpdate(BaseModel):
    email: EmailStr


class PhoneUpdate(BaseModel):
    phone_number: constr(pattern=r'^\+?1?\d{9,15}$')


class PasswordUpdate(BaseModel):
    password: str


class SpecializationEnum(str, Enum):
    cardiologist = 'tv'
    dermatologist = 'pc'


class SpecialistInput(BaseModel):
    last_name: str
    first_name: str
    middle_name: str
    email: EmailStr
    phone_number: constr(pattern=r'^\+?1?\d{9,15}$')
    password: str
    specialization: List[SpecializationEnum]


class Specialist(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    email: EmailStr
    phone_number: constr(pattern=r'^\+?1?\d{9,15}$')
    password: str
    specialization: List[SpecializationEnum]
    timestamp: datetime

    class Config:
        from_attributes = True
