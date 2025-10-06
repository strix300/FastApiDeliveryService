import asyncio
from app.core.db import engine, async_session
from app.db.models import Base
from app.db.models import ShipmentType 
from sqlalchemy import select

async def recreate_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await add_types_in_new_table()

async def create_tables_if_not_exist():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await add_types_in_new_table()
        
async def add_types_in_new_table():
    async with async_session() as session:
        result = await session.execute(select(ShipmentType))
        existing = {row.id for row in result.scalars().all()}

        default_types = [
            (1, "cloth"),
            (2, "electronics"),
            (3, "other"),
        ]

        for type_id, name in default_types:
            if type_id not in existing:
                session.add(ShipmentType(id=type_id, name=name))

        await session.commit()

if __name__ == "__main__":
    asyncio.run(recreate_tables())