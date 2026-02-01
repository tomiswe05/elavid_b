from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Schema for creating a new product (what the API accepts)
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    image_url: Optional[str] = None
    category: Optional[str] = None


# Schema for updating a product (all fields optional)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None
    category: Optional[str] = None


# Schema for returning product data (what the API sends back)
class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    image_url: Optional[str]
    category: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
