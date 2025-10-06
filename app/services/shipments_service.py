from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.db.models import Shipment
from app.db.types import ShipmentSchema
from app.utils.delivery_price import get_delivery_price
from fastapi import HTTPException

async def get_user_shipments_service(
    session: AsyncSession,
    session_id: str,
    page: int,
    limit: int,
    type_id: int | None = None,
    delivery_calculated: bool | None = None,
) -> dict:
    
    offset = (page - 1) * limit
    
    query = (select(Shipment).options(selectinload(Shipment.type)).where(Shipment.session_id == session_id))
    
    if type_id is not None:
        query = query.where(Shipment.type_id == type_id)
    if delivery_calculated is True:
        query = query.where(Shipment.delivery_cost.is_not(None))
    elif delivery_calculated is False:
        query = query.where(Shipment.delivery_cost.is_(None))
    
    result = await session.execute(query.limit(limit).offset(offset))
    shipments = result.scalars().all()
    
    total_result = await session.execute(
        select(func.count()).select_from(query.subquery())
    )
    total = total_result.scalar_one()
    
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "pages": (total + limit - 1) // limit,
        "items": [
            {
                "id": s.id,
                "name": s.name,
                "weight": s.weight,
                "content_cost": s.content_cost,
                "type": s.type.name,
                "delivery_cost": s.delivery_cost,
            }
            for s in shipments
        ],
    }
    
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

async def set_delivery_prices(session: AsyncSession):
    result = await session.execute(
        select(Shipment).where(Shipment.delivery_cost.is_(None))
    )
    shipments = result.scalars().all()
    
    for shipment in shipments:
        shipment.delivery_cost = await get_delivery_price(shipment.weight, shipment.content_cost)
    
    await session.commit()
    return len(shipments) 