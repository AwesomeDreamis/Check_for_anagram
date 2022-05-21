from fastapi import FastAPI, Query
import aioredis
import uvicorn
import asyncio
import custom_postgres_query

app = FastAPI()


async def set_counter_from_redis(val):
    redis = await aioredis.create_redis("redis://localhost:6379")
    await redis.set("counter", val)


async def get_counter_from_redis():
    redis = await aioredis.create_redis("redis://localhost:6379")
    value = await redis.get("counter")
    return value


def check_anagram(a, b):
    if sorted(a) == sorted(b):
        return True
    else:
        return False


# ==============================================================================

@app.get('/')
def get_info(first: str = Query(), second: str = Query()):
    counter = asyncio.run(get_counter_from_redis())
    if check_anagram(first, second):
        asyncio.run(set_counter_from_redis(int(counter) + 1))
        counter = asyncio.run(get_counter_from_redis())
        return {"is_anagram": True,
                "counter": counter}
    else:
        return {"is_anagram": False,
                "counter": counter}


@app.get('/get_dev/')
def get_dev_without_endpoints():
    result = asyncio.run(custom_postgres_query.get_dev_without_endpoints())
    return result


@app.post('/add_device/', status_code=201)
def add_device(add_device: str = Query(description="введите название устройства чтобы добавить в базу")):
    asyncio.run(custom_postgres_query.create_device())
    return 'success'


@app.post('/bind_endpoint/', status_code=201)
def add_device(dev_id: int = Query(description="id устройства"), comment: str = Query(description="комментарий")):
    asyncio.run(custom_postgres_query.add_endpoint(dev_id, comment))
    return 'success'


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
