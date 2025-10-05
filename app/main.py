from fastapi import FastAPI, APIRouter
from app.routes import shipments, types
import uvicorn

app = FastAPI(
    title="FastAPI Delivery Service",
    description="Микросервис для регистрации и расчета стоимости посылок",
    version="0.1.0",
)

v1_routers = APIRouter(prefix='/v1', tags=['v1'])

app.include_router(shipments.router, prefix="/shipments", tags=["shipments"])
app.include_router(types.router, prefix="/types", tags=["types"])

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)