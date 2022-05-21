import asyncio
import asyncpg
import random
import secrets


async def create_device():
    conn = await asyncpg.connect(host='localhost',
                                 port='5432',
                                 database='test',
                                 user='postgres',
                                 password='admin')

    dev_type = random.choices(population=['emeter', 'zigbee', 'lora', 'gsm'])
    dev_id = secrets.token_hex(48)
    query = f"INSERT INTO devices (dev_id, dev_type) VALUES ('{dev_id}', '{dev_type[0]}')"
    await conn.execute(query)
    await conn.close()


async def add_endpoints():
    conn = await asyncpg.connect(host='localhost',
                                 port='5432',
                                 database='test',
                                 user='postgres',
                                 password='admin')

    query = """INSERT INTO endpoints (device_id, comment)
               VALUES (6, 'test'),
                      (8, 'test'),
                      (10, 'test'),
                      (12, 'test'),
                      (13, 'test')"""
    await conn.execute(query)
    await conn.close()


async def add_endpoint(dev_id, comment):
    conn = await asyncpg.connect(host='localhost',
                                 port='5432',
                                 database='test',
                                 user='postgres',
                                 password='admin')

    query = f"INSERT INTO endpoints (device_id, comment) VALUES ({dev_id}, '{comment}')"
    await conn.execute(query)
    await conn.close()


async def get_dev_without_endpoints():
    conn = await asyncpg.connect(host='localhost',
                                 port='5432',
                                 database='test',
                                 user='postgres',
                                 password='admin')

    async with conn.transaction():
        res = {}
        async for row in conn.cursor("""SELECT d.dev_type, COUNT(d.dev_type)
                                        FROM devices d
                                        LEFT JOIN endpoints e
                                        ON d.id = e.device_id
                                        WHERE e.id IS NULL
                                        GROUP BY d.dev_type"""):
            res[row[0]] = row[1]
    await conn.close()
    return res

