import motor.motor_asyncio
import os
import asyncio

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/got10in")
FIXIE_URL = os.getenv("FIXIE_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI, io_loop=asyncio.get_event_loop(), proxy=FIXIE_URL)
database = client.got10in

subscriptions = database["subscriptions"]

def add_subscriber(email: str) -> bool:
    """Add a new subscriber to the database."""
    if not db.subscribers.find_one({"email": email}):
        db.subscribers.insert_one({"email": email})
        return True
    return False
