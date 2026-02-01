from pydantic import BaseModel
from typing import Optional


# Schema for adding a product to cart
class CartAdd(BaseModel):
    product_id: int
    quantity: int = 1


# Schema for updating cart item quantity
class CartUpdate(BaseModel):
    quantity: int


# Schema for returning cart item data (includes product details for display)
class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product_name: Optional[str] = None
    product_price: Optional[float] = None
    product_image: Optional[str] = None

    model_config = {"from_attributes": True}
