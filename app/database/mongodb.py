import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

class DataBase:
    client: AsyncIOMotorClient = None
    db = None

db = DataBase()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
    db.db = db.client.school_security
    print("Connected to MongoDB")

async def close_mongo_connection():
    if db.client is not None:
        db.client.close()
        print("Closed MongoDB connection")

def get_database():
    return db.db
