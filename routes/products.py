"""
Product API Routes
Handles all CRUD operations for products
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models import Product, ProductCreate, ProductUpdate
from database import products_collection
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("/", response_model=dict)
async def get_products(
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    brand: Optional[str] = None,
    minPrice: Optional[float] = None,
    maxPrice: Optional[float] = None,
    search: Optional[str] = None,
    featured: Optional[bool] = None,
    sort: Optional[str] = "newest"
):
    """
    Get products with filtering, pagination, and sorting
    
    Query Parameters:
    - page: Page number (default: 1)
    - pageSize: Items per page (default: 20, max: 100)
    - category: Filter by category
    - subcategory: Filter by subcategory
    - brand: Filter by brand
    - minPrice: Minimum price filter
    - maxPrice: Maximum price filter
    - search: Text search in name, description, tags
    - featured: Filter featured products
    - sort: Sort order (newest, price_asc, price_desc, popular)
    """
    # Build filter query
    query = {}
    
    if category:
        query["category"] = category
    if subcategory:
        query["subcategory"] = subcategory
    if brand:
        query["brand"] = brand
    if featured is not None:
        query["featured"] = featured
    if minPrice or maxPrice:
        query["price"] = {}
        if minPrice:
            query["price"]["$gte"] = minPrice
        if maxPrice:
            query["price"]["$lte"] = maxPrice
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"tags": {"$regex": search, "$options": "i"}}
        ]
    
    # Sorting
    sort_options = {
        "price_asc": ("price", 1),
        "price_desc": ("price", -1),
        "newest": ("createdAt", -1),
        "popular": ("reviewCount", -1)
    }
    sort_field, sort_order = sort_options.get(sort, ("createdAt", -1))
    
    # Count total
    total = await products_collection.count_documents(query)
    
    # Pagination
    skip = (page - 1) * pageSize
    
    # Fetch products
    cursor = products_collection.find(query).sort(sort_field, sort_order).skip(skip).limit(pageSize)
    products = await cursor.to_list(length=pageSize)
    
    # Convert ObjectId to string
    for product in products:
        product["_id"] = str(product["_id"])
    
    return {
        "data": products,
        "total": total,
        "page": page,
        "pageSize": pageSize,
        "totalPages": (total + pageSize - 1) // pageSize
    }

@router.get("/{product_id}")
async def get_product(product_id: str):
    """Get a single product by ID"""
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    product = await products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product["_id"] = str(product["_id"])
    return product

@router.post("/", status_code=201)
async def create_product(product: ProductCreate):
    """Create a new product"""
    product_dict = product.dict()
    product_dict["createdAt"] = datetime.utcnow()
    product_dict["updatedAt"] = datetime.utcnow()
    
    result = await products_collection.insert_one(product_dict)
    created_product = await products_collection.find_one({"_id": result.inserted_id})
    created_product["_id"] = str(created_product["_id"])
    
    return created_product

@router.put("/{product_id}")
async def update_product(product_id: str, product: ProductUpdate):
    """Update an existing product"""
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    update_data = {k: v for k, v in product.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    update_data["updatedAt"] = datetime.utcnow()
    
    result = await products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    updated_product = await products_collection.find_one({"_id": ObjectId(product_id)})
    updated_product["_id"] = str(updated_product["_id"])
    
    return updated_product

@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: str):
    """Delete a product"""
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    result = await products_collection.delete_one({"_id": ObjectId(product_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return None
