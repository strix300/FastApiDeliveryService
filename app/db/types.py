from pydantic import BaseModel, Field

class ShipmentTypeSchema(BaseModel):
    name: str
    
class ShipmentTypeAdd(ShipmentTypeSchema):
    id: int
    
class ShipmentSchema(BaseModel):
    name: str
    weight: float = Field(ge=0)
    content_cost: float = Field(ge=0)
    type_id: int
    
class ShipmentAdd(ShipmentSchema):
    id: int
    delivery_cost: float | None = None

class ShipmentResponse(BaseModel):
    id: int
    name: str
    weight: float = Field(ge=0)
    content_cost: float = Field(ge=0)
    type: str  
    delivery_cost: float | None = None

class ShipmentPaginatioResponse(BaseModel):
    page: int
    limit: int
    total: int
    pages: int
    items: list[ShipmentResponse]