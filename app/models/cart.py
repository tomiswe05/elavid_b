from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)  # Firebase UID
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)  # References products table
    quantity = Column(Integer, default=1)  # How many of this product the user wants

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
