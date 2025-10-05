from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.db.types import ShipmentTypeSchema
from app.services.shipment_types_service import get_list_types, create_shipment_type

router = APIRouter()

@router.get("/", response_model=list[dict])
async def get_types(session: AsyncSession = Depends(get_session)):
    return await get_list_types(session)

@router.post("/", response_model=ShipmentTypeSchema)
async def add_type(shipment_type_in: ShipmentTypeSchema, session: AsyncSession = Depends(get_session)):
    return await create_shipment_type(session, shipment_type_in)