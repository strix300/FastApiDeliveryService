from pydantic import BaseModel

class ShipmentTypeSchema(BaseModel):
    name: str
    
class ShipmentTypeAdd(ShipmentTypeSchema):
    id: int
    
class ShipmentSchema(BaseModel):
    name: str
    weight: float
    content_cost: float
    type_id: int
    
class ShipmentAdd(ShipmentSchema):
    id: int
    delivery_cost: float | None = None

class ShipmentResponse(BaseModel):
    id: int
    name: str
    weight: float
    content_cost: float
    type: str  
    delivery_cost: float | None = None

class ShipmentPaginatioResponse(BaseModel):
    page: int
    limit: int
    total: int
    pages: int
    items: list[ShipmentResponse]