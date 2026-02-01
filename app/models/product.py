from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)  # Available quantity in inventory
    image_url = Column(String, nullable=True)  # URL to product image
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # One product can appear in many carts
    cart_items = relationship("Cart", back_populates="product")
    # One product can appear in many order items
    order_items = relationship("OrderItem", back_populates="product")
