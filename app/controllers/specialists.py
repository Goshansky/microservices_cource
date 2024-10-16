from fastapi import HTTPException, APIRouter
from app.database.database import database
from app.models.models import specialists
from app.schemas.schemas import EmailUpdate, PhoneUpdate, PasswordUpdate, Specialist, SpecialistInput
from datetime import datetime
from sqlalchemy import update


router = APIRouter()

@router.post("/specialists", response_model=Specialist)
async def register_specialist(specialist: SpecialistInput):
    query = specialists.insert().values(
        last_name=specialist.last_name,
        first_name=specialist.first_name,
        middle_name=specialist.middle_name,
        email=specialist.email,
        phone_number=specialist.phone_number,
        password=specialist.password,
        specialization=specialist.specialization,
        timestamp=datetime.utcnow()
    )
    specialist_id = await database.execute(query)
    return {**specialist.dict(), "id": specialist_id, "timestamp": datetime.utcnow()}


@router.get("/specialists/{id}", response_model=Specialist)
async def get_specialist(id: int):
    query = specialists.select().where(specialists.c.id == id)
    specialist = await database.fetch_one(query)
    if not specialist:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return specialist


@router.put("/specialists/{id}/email", response_model=Specialist)
async def update_specialist_email(id: int, email_update: EmailUpdate):
    query = update(specialists).where(specialists.c.id == id).values(email=email_update.email)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return await get_specialist(id)


@router.put("/specialists/{id}/phone", response_model=Specialist)
async def update_specialist_phone(id: int, phone_update: PhoneUpdate):
    query = update(specialists).where(specialists.c.id == id).values(phone_number=phone_update.phone_number)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return await get_specialist(id)


@router.put("/specialists/{id}/password", response_model=Specialist)
async def change_specialist_password(id: int, password_update: PasswordUpdate):
    query = update(specialists).where(specialists.c.id == id).values(password=password_update.password)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return await get_specialist(id)
