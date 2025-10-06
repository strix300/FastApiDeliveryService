import asyncio
from aiokafka import AIOKafkaConsumer
import json
from app.core.db import async_session 
from app.services.shipments_service import set_delivery_prices

async def consume_delivery_tasks():
    consumer = AIOKafkaConsumer(
        "delivery_tasks",
        bootstrap_servers="kafka:9092",
        group_id="delivery_worker"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            data = json.loads(msg.value)
            if data.get("action") == "update_delivery_prices":
                async with async_session() as session:
                    count = await set_delivery_prices(session)
                    print(f"Updated {count} shipments")
    finally:
        await consumer.stop()