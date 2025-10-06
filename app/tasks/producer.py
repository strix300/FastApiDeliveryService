import asyncio
from aiokafka import AIOKafkaProducer
import json

async def periodic_producer():
    producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
    await producer.start()
    try:
        while True:
            message = {"action": "update_delivery_prices"}
            await producer.send_and_wait("delivery_tasks", json.dumps(message).encode("utf-8"))
            print("delivery_tasks produced")
            await asyncio.sleep(360)
    finally:
        await producer.stop()