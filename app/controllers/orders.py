from fastapi import HTTPException, APIRouter
from app.database.database import database
from app.models.models import orders
from app.schemas.schemas import Order, OrderInput, OrderStatusUpdate
from datetime import datetime
from sqlalchemy import update

router = APIRouter()


@router.post("/orders", response_model=Order)
async def create_order(order: OrderInput):
    query = orders.insert().values(
        client_pk=order.client_pk,
        specialist_pk=order.specialist_pk,
        specialization=order.specialization,
        status=order.status,
        comment=order.comment,
        timestamp=datetime.utcnow()
    )
    order_id = await database.execute(query)
    return {**order.dict(), "id": order_id, "timestamp": datetime.utcnow()}


@router.get("/orders/{id}", response_model=Order)
async def get_order(id: int):
    query = orders.select().where(orders.c.id == id)
    order = await database.fetch_one(query)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/orders/{id}/status", response_model=Order)
async def update_order_status(id: int, status_update: OrderStatusUpdate):
    query = update(orders).where(orders.c.id == id).values(status=status_update.status)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return await get_order(id)
