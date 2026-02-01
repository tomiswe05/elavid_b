from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


# Schema for returning a single item within an order
class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float  # Price at time of purchase

    model_config = {"from_attributes": True}


# Schema for returning an order with its items
class OrderOut(BaseModel):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    order_items: List[OrderItemOut] = []

    model_config = {"from_attributes": True}


# Schema for returning payment info
class PaymentOut(BaseModel):
    id: int
    order_id: int
    payment_ref: Optional[str]
    status: str
    provider: Optional[str]

    model_config = {"from_attributes": True}


# Schema for returning the Stripe Checkout session URL
class CheckoutSessionOut(BaseModel):
    checkout_url: str
    session_id: str
