import motor.motor_asyncio
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/got10in")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client.got10in
