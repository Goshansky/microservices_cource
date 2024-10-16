from pydantic import BaseModel, EmailStr, constr
from datetime import datetime


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
