"""
Category API Routes
Handles category operations
"""
from fastapi import APIRouter, HTTPException
from typing import List
from models import Category, CategoryCreate
from database import categories_collection
from bson import ObjectId

router = APIRouter(prefix="/api/categories", tags=["categories"])

@router.get("/", response_model=List[dict])
async def get_categories():
    """Get all categories"""
    cursor = categories_collection.find({})
    categories = await cursor.to_list(length=100)
    
    # Convert ObjectId to string
    for category in categories:
        category["_id"] = str(category["_id"])
    
    return categories

@router.get("/{category_id}")
async def get_category(category_id: str):
    """Get a single category by ID"""
    if not ObjectId.is_valid(category_id):
        raise HTTPException(status_code=400, detail="Invalid category ID")
    
    category = await categories_collection.find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category["_id"] = str(category["_id"])
    return category

@router.post("/", status_code=201)
async def create_category(category: CategoryCreate):
    """Create a new category"""
    # Check if slug already exists
    existing = await categories_collection.find_one({"slug": category.slug})
    if existing:
        raise HTTPException(status_code=400, detail="Category slug already exists")
    
    category_dict = category.dict()
    result = await categories_collection.insert_one(category_dict)
    created_category = await categories_collection.find_one({"_id": result.inserted_id})
    created_category["_id"] = str(created_category["_id"])
    
    return created_category

@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: str):
    """Delete a category"""
    if not ObjectId.is_valid(category_id):
        raise HTTPException(status_code=400, detail="Invalid category ID")
    
    result = await categories_collection.delete_one({"_id": ObjectId(category_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return None
