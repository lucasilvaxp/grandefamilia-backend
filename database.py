"""
MongoDB Database Configuration
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# CRITICAL: Read from environment variable to prevent KeyError
MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise ValueError("MONGO_URL environment variable is required but not set")

DB_NAME = os.getenv("MONGO_DB_NAME", "fashion_catalog")

# Async MongoDB client for FastAPI
client = AsyncIOMotorClient(MONGO_URL)
database = client[DB_NAME]

# Collections
products_collection = database.get_collection("products")
categories_collection = database.get_collection("categories")

async def get_database():
    """Get database instance"""
    return database

async def init_indexes():
    """Initialize database indexes for performance"""
    # Products indexes
    await products_collection.create_index("category")
    await products_collection.create_index("brand")
    await products_collection.create_index("price")
    await products_collection.create_index("featured")
    await products_collection.create_index([("createdAt", -1)])
    
    # Text search index
    await products_collection.create_index([
        ("name", "text"),
        ("description", "text"),
        ("tags", "text")
    ])
    
    # Categories indexes
    await categories_collection.create_index("slug", unique=True)
    
    print("✅ Database indexes initialized successfully")

# Initialize indexes on startup (call this in main.py if needed)
