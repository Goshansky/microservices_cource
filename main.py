from fastapi import FastAPI, HTTPException
from database import database, engine, metadata
from models import clients, specialists
from schemas import ClientInput, Client, EmailUpdate, PhoneUpdate, PasswordUpdate, Specialist, SpecialistInput
from datetime import datetime
import uvicorn
from contextlib import asynccontextmanager
from sqlalchemy import update


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"Проверка": "Проверка"}


@app.post("/clients", response_model=Client)
async def register_client(client: ClientInput):
    query = clients.insert().values(
        last_name=client.last_name,
        first_name=client.first_name,
        middle_name=client.middle_name,
        email=client.email,
        phone_number=client.phone_number,
        password=client.password,
        timestamp=datetime.utcnow()
    )
    client_id = await database.execute(query)
    return {**client.dict(), "id": client_id, "timestamp": datetime.utcnow()}


@app.get("/clients/{id}", response_model=Client)
async def get_client(id: int):
    query = clients.select().where(clients.c.id == id)
    client = await database.fetch_one(query)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@app.put("/clients/{id}/email", response_model=Client)
async def update_client_email(id: int, email_update: EmailUpdate):
    query = update(clients).where(clients.c.id == id).values(email=email_update.email)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    return await get_client(id)


@app.put("/clients/{id}/phone", response_model=Client)
async def update_client_phone(id: int, phone_update: PhoneUpdate):
    query = update(clients).where(clients.c.id == id).values(phone_number=phone_update.phone_number)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    return await get_client(id)


@app.put("/clients/{id}/password", response_model=Client)
async def change_client_password(id: int, password_update: PasswordUpdate):
    query = update(clients).where(clients.c.id == id).values(password=password_update.password)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    return await get_client(id)


@app.post("/specialists", response_model=Specialist)
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


@app.get("/specialists/{id}", response_model=Specialist)
async def get_specialist(id: int):
    query = specialists.select().where(specialists.c.id == id)
    specialist = await database.fetch_one(query)
    if not specialist:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return specialist

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
