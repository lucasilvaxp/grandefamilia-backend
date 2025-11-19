from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
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
brands_collection = db.brands

class BrandCreate(BaseModel):
    name: str
    description: Optional[str] = None
    logo: Optional[str] = None

class BrandUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[str] = None

@router.get("/brands")
async def get_brands():
    """Get all brands"""
    try:
        brands = []
        async for brand in brands_collection.find():
            brand["_id"] = str(brand["_id"])
            brands.append(brand)
        return JSONResponse(content=brands)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/brands/{brand_id}")
async def get_brand(brand_id: str):
    """Get a single brand by ID"""
    try:
        brand = await brands_collection.find_one({"_id": ObjectId(brand_id)})
        if not brand:
            raise HTTPException(status_code=404, detail="Marca não encontrada")
        brand["_id"] = str(brand["_id"])
        return JSONResponse(content=brand)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/brands")
async def create_brand(brand: BrandCreate):
    """Create a new brand"""
    try:
        brand_dict = brand.dict()
        brand_dict["createdAt"] = datetime.utcnow().isoformat()
        brand_dict["updatedAt"] = datetime.utcnow().isoformat()
        
        result = await brands_collection.insert_one(brand_dict)
        brand_dict["_id"] = str(result.inserted_id)
        
        return JSONResponse(content=brand_dict, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/brands/{brand_id}")
async def update_brand(brand_id: str, brand: BrandUpdate):
    """Update a brand"""
    try:
        update_data = {k: v for k, v in brand.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado para atualizar")
        
        update_data["updatedAt"] = datetime.utcnow().isoformat()
        
        result = await brands_collection.update_one(
            {"_id": ObjectId(brand_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Marca não encontrada")
        
        updated_brand = await brands_collection.find_one({"_id": ObjectId(brand_id)})
        updated_brand["_id"] = str(updated_brand["_id"])
        
        return JSONResponse(content=updated_brand)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/brands/{brand_id}")
async def delete_brand(brand_id: str):
    """Delete a brand"""
    try:
        result = await brands_collection.delete_one({"_id": ObjectId(brand_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Marca não encontrada")
        
        return JSONResponse(content={"message": "Marca deletada com sucesso"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
