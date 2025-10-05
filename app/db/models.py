from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    pass

class ShipmentType(Base):
    __tablename__ = "shipment_types"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

class Shipment(Base):
    __tablename__ = "shipments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    content_cost: Mapped[float] = mapped_column(nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("shipment_types.id"))
    type: Mapped[ShipmentType] = relationship()
    delivery_cost: Mapped[float] = mapped_column(nullable=True)
    session_id: Mapped[str] = mapped_column(nullable=False)