from fastapi import FastAPI, HTTPException
from database import database, engine, metadata
from models import clients
from schemas import ClientInput, Client
from datetime import datetime
import uvicorn
from contextlib import asynccontextmanager


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
