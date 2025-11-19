"""
Pydantic Models for Request/Response Validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Color(BaseModel):
    """Color model"""
    name: str
    hex: str

class ProductBase(BaseModel):
    """Base product model with all fields"""
    name: str
    description: str
    price: float
    originalPrice: Optional[float] = None
    category: str
    subcategory: Optional[str] = None
    brand: str
    sizes: List[str]
    colors: List[Color]
    images: List[str]
    stock: int
    featured: bool = False
    tags: Optional[List[str]] = []
    rating: Optional[float] = None
    reviewCount: Optional[int] = 0

class ProductCreate(ProductBase):
    """Model for creating a new product"""
    pass

class ProductUpdate(BaseModel):
    """Model for updating an existing product (all fields optional)"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    originalPrice: Optional[float] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    sizes: Optional[List[str]] = None
    colors: Optional[List[Color]] = None
    images: Optional[List[str]] = None
    stock: Optional[int] = None
    featured: Optional[bool] = None
    tags: Optional[List[str]] = None
    rating: Optional[float] = None
    reviewCount: Optional[int] = None

class Product(ProductBase):
    """Complete product model with ID and timestamps"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Category(BaseModel):
    """Category model"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    slug: str
    subcategories: Optional[List[str]] = []
    image: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class CategoryCreate(BaseModel):
    """Model for creating a new category"""
    name: str
    slug: str
    subcategories: Optional[List[str]] = []
    image: Optional[str] = None
