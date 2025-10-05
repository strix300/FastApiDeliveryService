from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.models import Shipment
from app.db.types import ShipmentSchema
from fastapi import HTTPException

async def get_user_shipments_service(session: AsyncSession, session_id: str) -> list[dict]:
    result = await session.execute(
        select(Shipment).options(selectinload(Shipment.type))
        .where(Shipment.session_id == session_id)
    )
    shipments = result.scalars().all()
    return [
    {
        "id": s.id,
        "name": s.name,
        "weight": s.weight,
        "content_cost": s.content_cost,
        "type": s.type.name,
        "delivery_cost": s.delivery_cost,
    }
    for s in shipments
]
    
async def get_shipment_service(shipment_id: int, session: AsyncSession, session_id: str) -> list[dict]:
    result = await session.execute(
        select(Shipment).options(selectinload(Shipment.type))
        .where(Shipment.id == shipment_id, Shipment.session_id == session_id)
    )
    shipment = result.scalars().all()
    
    if not shipment:
        raise HTTPException(status_code=404, detail="Посылка не найдена или не принадлежит пользователю")

    return [
    {
        "id": s.id,
        "name": s.name,
        "weight": s.weight,
        "content_cost": s.content_cost,
        "type": s.type.name,
        "delivery_cost": s.delivery_cost,
    }
    for s in shipment
]    

async def create_shipment_service(session: AsyncSession, shipment: ShipmentSchema, session_id: str):
    new_shipment = Shipment(
        name=shipment.name,
        weight=shipment.weight,
        content_cost=shipment.content_cost,
        type_id=shipment.type_id,
        delivery_cost=None,
        session_id=session_id
    )
    session.add(new_shipment)
    await session.commit()
    await session.refresh(new_shipment)
    return new_shipment