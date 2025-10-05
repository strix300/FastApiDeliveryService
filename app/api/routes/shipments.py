from fastapi import APIRouter, Request, Response
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.utils.session_id import get_or_create_session
from app.services.shipments_service import get_user_shipments_service, create_shipment_service, get_shipment_service
from app.db.types import ShipmentSchema, ShipmentAdd, ShipmentResponse

router = APIRouter()

@router.get("/", response_model=list[ShipmentResponse])
async def get_user_shipments(request: Request, response: Response, session: AsyncSession = Depends(get_session)):
    session_id = await get_or_create_session(request=request, response=response)
    return await get_user_shipments_service(session, session_id)

@router.get("/{shipment_id}", response_model=list[ShipmentResponse])
async def get_user_shipments(shipment_id: int, request: Request, response: Response, session: AsyncSession = Depends(get_session)):
    session_id = await get_or_create_session(request=request, response=response)
    return await get_shipment_service(shipment_id, session, session_id)

@router.post("/")
async def add_user_shipment(shipment: ShipmentSchema, request: Request, response: Response, session: AsyncSession = Depends(get_session)):
    session_id = await get_or_create_session(request=request, response=response)
    new_shipment = await create_shipment_service(session, shipment, session_id)
    return new_shipment

