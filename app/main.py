from fastapi import FastAPI, APIRouter
from app.routes import shipments, types
from app.tasks.producer import periodic_producer
from app.tasks.consumer import consume_delivery_tasks
import uvicorn
import asyncio
from app.db.recreate_tables import create_tables_if_not_exist

v1_routers = APIRouter(prefix="/v1", tags=["v1"])
v1_routers.include_router(shipments.router, prefix="/shipments", tags=["🚚 shipments"])
v1_routers.include_router(types.router, prefix="/types", tags=["📂 types"])

app = FastAPI(
    title="FastAPI Delivery Service",
    description="Микросервис для регистрации и расчета стоимости посылок",
    version="0.1.0",
)

app.include_router(v1_routers)

@app.on_event("startup")
async def startup_event():
    await create_tables_if_not_exist()
    
    asyncio.create_task(periodic_producer())
    asyncio.create_task(consume_delivery_tasks())