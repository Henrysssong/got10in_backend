import motor.motor_asyncio
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/got10in")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client.got10in

subscriptions = database["subscriptions"]
# db/mongo.py

def add_subscriber(email: str) -> bool:
    """Add a new subscriber to the database."""
    if not db.subscribers.find_one({"email": email}):
        db.subscribers.insert_one({"email": email})
        return True
    return False
