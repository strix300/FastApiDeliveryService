import httpx
import redis.asyncio as redis

redis_client = redis.Redis(host="redis", port=6379, db=0)

async def get_exchange_rate(valute: str = 'USD') -> float:
    rate = await redis_client.get("usd_rate")
    if rate is None:
        async with httpx.AsyncClient() as client:
            url = "https://www.cbr-xml-daily.ru/daily_json.js"
            response = await client.get(url)
            data = response.json()
            usd_rate = data['Valute'][valute]['Value']
            await redis_client.set("usd_rate", usd_rate, ex=1800)
            return float(usd_rate)
    return float(rate)
    
async def get_delivery_price(weight: float, content_cost: float) -> float:
    exchange_rate = await get_exchange_rate()
    price = (weight * 0.5 + content_cost * 0.01) * exchange_rate
    return price