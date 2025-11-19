"""
Store Settings API Routes
Handles store configuration
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from datetime import datetime
import os
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.fashion_catalog
settings_collection = db.settings

class StoreSettingsUpdate(BaseModel):
    storeName: Optional[str] = None
    whatsappNumber: Optional[str] = None
    whatsappMessage: Optional[str] = None
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

@router.get("/settings")
async def get_settings():
    """Get store settings"""
    try:
        settings = await settings_collection.find_one({"type": "store"})
        if not settings:
            # Return default settings if none exist
            default_settings = {
                "type": "store",
                "storeName": "Loja A Grande Família",
                "whatsappNumber": "5593991084582",
                "whatsappMessage": "Olá! Gostaria de saber mais sobre os produtos.",
                "instagram": "",
                "facebook": "",
                "email": "",
                "address": "",
                "createdAt": datetime.utcnow().isoformat(),
                "updatedAt": datetime.utcnow().isoformat()
            }
            await settings_collection.insert_one(default_settings)
            settings = default_settings
        
        if "_id" in settings:
            settings["_id"] = str(settings["_id"])
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/settings")
async def update_settings(settings: StoreSettingsUpdate):
    """Update store settings"""
    try:
        update_data = {k: v for k, v in settings.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado para atualizar")
        
        update_data["updatedAt"] = datetime.utcnow().isoformat()
        
        # Upsert settings
        result = await settings_collection.update_one(
            {"type": "store"},
            {"$set": update_data},
            upsert=True
        )
        
        updated_settings = await settings_collection.find_one({"type": "store"})
        if "_id" in updated_settings:
            updated_settings["_id"] = str(updated_settings["_id"])
        
        return updated_settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
