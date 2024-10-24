from fastapi import FastAPI
from app.database.database import database, engine, metadata
from app.controllers import orders, clients, specialists
from config.config import APP_PORT, APP_HOST
import uvicorn
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(orders.router)
app.include_router(clients.router)
app.include_router(specialists.router)


@app.get("/")
async def read_root():
    return {"Проверка": "Проверка"}


if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
