from fastapi import HTTPException, APIRouter
from app.database.database import database
from app.models.models import clients, orders
from app.schemas.schemas import ClientInput, Client, EmailUpdate, PhoneUpdate, PasswordUpdate, Order
from datetime import datetime
from sqlalchemy import update, select


router = APIRouter()


@router.post("/clients", response_model=Client)
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


@router.get("/clients/{id}", response_model=Client)
async def get_client(id: int):
    query = clients.select().where(clients.c.id == id)
    client = await database.fetch_one(query)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/clients/{id}/email", response_model=Client)
async def update_client_email(id: int, email_update: EmailUpdate):
    query = update(clients).where(clients.c.id == id).values(email=email_update.email)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    return await get_client(id)


@router.put("/clients/{id}/phone", response_model=Client)
async def update_client_phone(id: int, phone_update: PhoneUpdate):
    query = update(clients).where(clients.c.id == id).values(phone_number=phone_update.phone_number)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    return await get_client(id)


@router.put("/clients/{id}/password", response_model=Client)
async def change_client_password(id: int, password_update: PasswordUpdate):
    query = update(clients).where(clients.c.id == id).values(password=password_update.password)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    return await get_client(id)


@router.get("/clients/{client_id}/orders", response_model=list[Order])
async def get_client_orders(client_id: int):
    query = select(orders).where(orders.c.client_pk == client_id)
    client_orders = await database.fetch_all(query)
    if not client_orders:
        raise HTTPException(status_code=404, detail="No orders found for this client")
    return client_orders
