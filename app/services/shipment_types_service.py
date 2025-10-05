from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import ShipmentType
from app.db.types import ShipmentTypeSchema
from fastapi import HTTPException

async def get_list_types(session: AsyncSession) -> list[dict]:
    result = await session.execute(select(ShipmentType))
    types = result.scalars().all()
    return [{"id": t.id, "name": t.name} for t in types]

async def create_shipment_type(session: AsyncSession, shipment_type_in: ShipmentTypeSchema):
    result = await session.execute(select(ShipmentType).where(ShipmentType.name == shipment_type_in.name))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Тип посылки уже существует")

    new_type = ShipmentType(name=shipment_type_in.name)
    session.add(new_type)
    await session.commit()
    await session.refresh(new_type)
    return new_type